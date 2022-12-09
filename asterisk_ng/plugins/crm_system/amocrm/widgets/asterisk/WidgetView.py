from typing import Any
from typing import Mapping
from typing import Optional
from pydantic import Field
from fastapi import Request
from fastapi import Response

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IOriginationDomainCommand
from asterisk_ng.interfaces import IGetCrmUserIdByPhoneQuery

from .AsteriskPluginConfig import AsteriskPluginConfig


__all__ = ["WidgetView"]


class WidgetView:

    __slots__ = (
        "__config",
        "__origination_command",
        "__get_crm_user_id_by_phone_query",
    )

    def __init__(
        self,
        config: AsteriskPluginConfig,
        origination_command: IOriginationDomainCommand,
        get_crm_user_id_by_phone_query: IGetCrmUserIdByPhoneQuery,
    ) -> None:
        self.__config = config
        self.__origination_command = origination_command
        self.__get_crm_user_id_by_phone_query = get_crm_user_id_by_phone_query

    def __make_response(
        self,
        data: Optional[Mapping[str, Any]] = None
    ) -> Response:
        data = data or {}
        response = Response(
            content=f"asterisk_cb({str(data)});",
            media_type="text/javascript",
        )
        return response

    async def handle(self, request: Request) -> Response:

        request_params = request.query_params

        try:
            login = request_params["_login"]
            password = request_params["_secret"]
            action = request_params["_action"]
        except KeyError:
            return self.__make_response({"status": "invalid data."})

        if login != self.__config.login or password != self.__config.password:
            return self.__make_response({"status": "not authorized."})

        if action == "status":
            return self.__make_response({"status": "ok"})

        if action == "cdr":
            return self.__make_response({"status": "no cdr."})

        if action == "call":
            try:
                caller_phone_number = request_params["from"]
                called_phone_number = request_params["to"]
            except KeyError:
                return self.__make_response({"status": "invalid data."})

            try:
                user_id = await self.__get_crm_user_id_by_phone_query(caller_phone_number)
            except KeyError:
                return self.__make_response({"status": "unknown agent number."})

            await self.__origination_command(
                user_id=user_id,
                phone_number=called_phone_number,
            )

            return self.__make_response({"status": "ok"})

        return self.__make_response({"status": "unknown action."})

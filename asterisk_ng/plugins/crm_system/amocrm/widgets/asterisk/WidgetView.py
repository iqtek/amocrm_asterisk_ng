from typing import Any
from typing import Mapping
from typing import Optional

from fastapi import Query
from fastapi import Response

from asterisk_ng.interfaces import IGetCrmUserIdByPhoneQuery
from asterisk_ng.interfaces import IOriginationDomainCommand
from .AsteriskPluginConfig import AsteriskPluginConfig


__all__ = ["WidgetView"]


class WidgetView:

    __PHONE_MIN_LENGTH = 3

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

    async def handle(
        self,
        login: str = Query(alias="_login"),
        password: str = Query(alias="_secret"),
        action: str = Query(alias="_action"),
        caller: Optional[str] = Query(None, alias="from"),
        called: Optional[str] = Query(None, alias="to"),
    ) -> Response:

        if login != self.__config.login or password != self.__config.password:
            return self.__make_response({"status": "not authorized."})

        if action == "status":
            return self.__make_response({"status": "ok"})

        if action == "cdr":
            return self.__make_response({"status": "no cdr."})

        if action == "call":
            if caller is None or called is None:
                return self.__make_response({"status": "invalid data."})

            if len(caller) < self.__PHONE_MIN_LENGTH or len(called) < self.__PHONE_MIN_LENGTH:
                return self.__make_response({"status": "invalid phones."})

            try:
                user_id = await self.__get_crm_user_id_by_phone_query(caller)
            except KeyError:
                return self.__make_response({"status": "unknown agent number."})

            await self.__origination_command(
                user_id=user_id,
                phone_number=called,
            )

            return self.__make_response({"status": "ok"})

        return self.__make_response({"status": "unknown action."})

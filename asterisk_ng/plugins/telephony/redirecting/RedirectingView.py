from typing import Optional

from fastapi.responses import PlainTextResponse

from asterisk_ng.interfaces import IGetResponsibleUserByPhoneQuery


__all__ = ["RedirectingView"]


class RedirectingView:

    __slots__ = (
        "__get_responsible_user_by_phone_query",
    )

    def __init__(
        self,
        get_responsible_user_by_phone_query: IGetResponsibleUserByPhoneQuery,
    ) -> None:
        self.__get_responsible_user_by_phone_query = get_responsible_user_by_phone_query

    def __make__response(self, content: Optional[str] = None) -> PlainTextResponse:
        return PlainTextResponse(
            content=content,
            status_code=200,
        )

    async def handle(self, phone: Optional[str] = None) -> PlainTextResponse:

        if phone is None:
            return self.__make__response()

        try:
            responsible_user_phone_number = await self.__get_responsible_user_by_phone_query(client_phone=phone)
        except KeyError:
            return self.__make__response()

        return self.__make__response(content=responsible_user_phone_number)

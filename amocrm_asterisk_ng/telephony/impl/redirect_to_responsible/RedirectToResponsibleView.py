from typing import Optional

from fastapi.responses import PlainTextResponse

from amocrm_asterisk_ng.domain import IGetResponsibleUserByPhoneQuery


__all__ = [
    "RedirectToResponsibleView"
]


class RedirectToResponsibleView:

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

    async def handle(self, responsible_user: Optional[str] = None) -> PlainTextResponse:
        if responsible_user is None:
            return self.__make__response()
        try:
            responsible_user_phone_number = await self.__get_responsible_user_by_phone_query(
                phone_number=responsible_user,
            )
        except Exception:
            return self.__make__response()

        return self.__make__response(
            content=responsible_user_phone_number,
        )

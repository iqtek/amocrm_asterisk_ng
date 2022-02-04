from fastapi import Response

from fastapi.responses import JSONResponse
from asterisk_amocrm.domains import GetCdrByUniqueIdQuery
from asterisk_amocrm.domains.models import File, Filetype
from asterisk_amocrm.infrastructure import IDispatcher, ILogger


__all__ = [
    "CallRecordsView",
]


class CallRecordsView:

    def __init__(
        self,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__dispatcher = dispatcher
        self.__logger = logger

    async def handle(self, unique_id: str) -> Response:
        self.__logger.debug(
            f"CallRecordsView: request cdr for "
            f"unique_id: {unique_id}."
        )
        query = GetCdrByUniqueIdQuery(
            unique_id=unique_id,
            file_type=Filetype.MP3,
        )
        try:
            file: File = await self.__dispatcher.on_query(query)
        except FileNotFoundError:
            self.__logger.debug(
                f"CallRecordsView: cdr for "
                f"unique_id: {unique_id} not found."
            )
            return JSONResponse(
                status_code=404,
                content={"result": "file not found"},
            )
        return Response(content=file.content, media_type="audio/mp3")

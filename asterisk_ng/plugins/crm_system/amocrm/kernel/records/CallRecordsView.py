from fastapi import Response
from fastapi.responses import JSONResponse

from asterisk_ng.interfaces import File
from asterisk_ng.interfaces import Filetype
from asterisk_ng.interfaces import IGetRecordFileUniqueIdQuery

from asterisk_ng.system.logger import ILogger

from asterisk_ng.plugins.system.converter import IFileConverter


__all__ = ["CallRecordsView"]


class CallRecordsView:

    __slots__ = (
        "__get_record_file_unique_id_query",
        "__file_converter",
        "__logger",
        "__enable_conversion",
    )

    def __init__(
        self,
        get_record_file_unique_id_query: IGetRecordFileUniqueIdQuery,
        file_converter: IFileConverter,
        logger: ILogger,
        enable_conversion: bool = True,
    ) -> None:
        self.__get_record_file_unique_id_query = get_record_file_unique_id_query
        self.__file_converter = file_converter
        self.__logger = logger
        self.__enable_conversion = enable_conversion

    async def handle(self, unique_id: str) -> Response:
        try:
            file: File = await self.__get_record_file_unique_id_query(unique_id)
        except FileNotFoundError:
            return JSONResponse(
                status_code=404,
                content={"result": "file not found."},
            )

        if self.__enable_conversion:
            try:
                converted_file = await self.__file_converter.convert(
                    file=file,
                    new_filetype=Filetype.MP3,
                )
            except Exception as exc:
                await self.__logger.error(
                    "Error during file conversion "
                    f"file_name: `{file.name}` "
                    f"file_type: `{file.type}`.",
                    exception=exc,
                )
                return JSONResponse(
                    status_code=500,
                    content={"result": "File conversion error."},
                )
        else:
            converted_file = file

        return Response(
            content=converted_file.content,
            media_type=converted_file.type.value,
        )

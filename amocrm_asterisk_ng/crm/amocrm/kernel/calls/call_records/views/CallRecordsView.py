from fastapi import Response
from fastapi.responses import JSONResponse
from glassio.logger import ILogger

from amocrm_asterisk_ng.domain import File
from amocrm_asterisk_ng.domain import Filetype
from amocrm_asterisk_ng.domain import IGetRecordFileUniqueIdQuery

from ..CallRecordsConfig import CallRecordsConfig
from ..file_converters import IFileConverter


__all__ = [
    "CallRecordsView",
]


class CallRecordsView:

    __slots__ = (
        "__config",
        "__get_cdr_by_unique_id_query",
        "__file_converter",
        "__logger",
    )

    def __init__(
        self,
        config: CallRecordsConfig,
        get_cdr_by_unique_id_query: IGetRecordFileUniqueIdQuery,
        file_converter: IFileConverter,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__get_cdr_by_unique_id_query = get_cdr_by_unique_id_query
        self.__file_converter = file_converter
        self.__logger = logger

    async def handle(self, unique_id: str) -> Response:
        try:
            file: File = await self.__get_cdr_by_unique_id_query(
                unique_id=unique_id,
            )
        except FileNotFoundError as e:
            return JSONResponse(
                status_code=404,
                content={"result": "file not found."},
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={}
            )

        if self.__config.enable_conversion:
            try:
                converted_file = await self.__file_converter.convert(
                    file=file,
                    new_filetype=Filetype.MP3,
                )
            except Exception as exc:
                await self.__logger.warning(
                    "CallRecordsView: "
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

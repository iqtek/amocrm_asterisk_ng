import os
from typing import Any
from typing import Coroutine
from typing import Callable
import aiofiles
from aiomysql.connection import Cursor

from asterisk_ng.interfaces import File
from asterisk_ng.interfaces import Filetype
from asterisk_ng.interfaces import IGetRecordFileByUniqueIdQuery
from asterisk_ng.system.logger import ILogger

from .configs import RecordsProviderPluginConfig
from .utils import is_valid_unique_id


__all__ = ["GetRecordFileByUniqueIdQuery"]


class GetRecordFileByUniqueIdQuery(IGetRecordFileByUniqueIdQuery):

    __EXTENSIONS = {
        "mp3": Filetype.MP3,
        "mp4": Filetype.MP3,
        "wav": Filetype.WAV,
        "wave": Filetype.WAVE,
    }

    __slots__ = (
        "__config",
        "__get_cursor",
        "__logger",
    )

    def __init__(
        self,
        config: RecordsProviderPluginConfig,
        get_cursor: Callable[[], Coroutine[Any, Any, Cursor]],
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__get_cursor = get_cursor
        self.__logger = logger

    @classmethod
    async def __get_content_from_file(cls, path: str) -> bytes:
        async with aiofiles.open(path, mode='rb') as f:
            content = await f.read()
        return content

    async def __call__(self, unique_id: str) -> File:

        if not is_valid_unique_id(unique_id):
            raise ValueError(f"Invalid unique_id: `{unique_id}`.")

        cur = await self.__get_cursor()
        await cur.execute(
            f"SELECT {self.__config.calldate_column}, "
            f"{self.__config.recordingfile_column} "
            f"FROM {self.__config.cdr_table} WHERE uniqueid={unique_id}"
        )

        try:
            date, filename = await cur.fetchone()
        except TypeError:
            raise FileNotFoundError(f"File with unique_id: `{unique_id}` not found.")
        finally:
            await cur.close()

        if not date or not filename:
            raise FileNotFoundError(f"File with unique_id: `{unique_id}` not found.")

        directory_path = date.strftime(self.__config.media_root).rstrip('/')
        file_path = os.path.join(directory_path, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File with unique_id: `{unique_id}` not found,  file_path: `{file_path}`."
            )

        content = await self.__get_content_from_file(file_path)

        extension = filename.split(".")[-1]
        filetype = self.__EXTENSIONS[extension]

        return File(
            name=filename,
            type=filetype,
            content=content,
        )

import os
from typing import Any
from typing import Coroutine
from typing import Callable
from typing import Optional
from typing import Tuple

import aiofiles
from aiomysql.connection import Connection
from pymysql.err import MySQLError
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
        "__get_connection",
        "__connection",
        "__logger",
    )

    def __init__(
        self,
        config: RecordsProviderPluginConfig,
        get_connection: Callable[[], Coroutine[Any, Any, Connection]],
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__get_connection = get_connection
        self.__logger = logger
        self.__connection: Optional[Connection] = None

    @classmethod
    async def __get_content_from_file(cls, path: str) -> bytes:
        async with aiofiles.open(path, mode='rb') as f:
            content = await f.read()
        return content

    async def __get_fileinfo(self, unique_id: str) -> Tuple[str, str]:
        cur = self.__connection.cursor()
        await cur.execute(
            f"SELECT {self.__config.calldate_column}, "
            f"{self.__config.recordingfile_column} "
            f"FROM {self.__config.cdr_table} WHERE uniqueid={unique_id}"
        )

        try:
            date, filename = await cur.fetchone()
            return date, filename
        except TypeError:
            raise FileNotFoundError(f"File with unique_id: `{unique_id}` not found.")
        finally:
            await cur.close()

    async def __call__(self, unique_id: str) -> File:
        if not is_valid_unique_id(unique_id):
            raise ValueError(f"Invalid unique_id: `{unique_id}`.")

        if self.__connection is None:
            self.__connection = await self.__get_connection()

        try:
            date, filename = await self.__get_fileinfo(unique_id=unique_id)
        except (RuntimeError, MySQLError):
            self.__connection = await self.__get_connection()
            date, filename = await self.__get_fileinfo(unique_id=unique_id)

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

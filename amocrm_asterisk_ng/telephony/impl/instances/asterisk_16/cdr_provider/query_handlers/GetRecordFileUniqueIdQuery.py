import os

import aiofiles

from amocrm_asterisk_ng.domain import File
from amocrm_asterisk_ng.domain import Filetype
from amocrm_asterisk_ng.domain import IGetRecordFileUniqueIdQuery
from glassio.logger import ILogger

from ..CdrProviderConfig import CdrProviderConfig
from ..mysql import MySqlConnectionFactoryImpl


__all__ = [
    "GetRecordFileUniqueIdQuery.py",
]


class GetRecordFileUniqueIdQuery(IGetRecordFileUniqueIdQuery):

    __slots__ = (
        "__config",
        "__mysql_connection_factory",
        "__logger",
    )

    def __init__(
        self,
        config: CdrProviderConfig,
        mysql_connection_factory: MySqlConnectionFactoryImpl,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__mysql_connection_factory = mysql_connection_factory
        self.__logger = logger

    @classmethod
    async def __get_content_from_file(
        cls,
        path: str
    ) -> bytes:
        async with aiofiles.open(
            path,
            mode='rb',
        ) as f:
            content = await f.read()
        return content

    async def __call__(
        self,
        unique_id: str,
    ) -> File:
        try:
            conn = await self.__mysql_connection_factory.get_instance(
                settings=self.__config.mysql,
            )
        except Exception as e:
            await self.__logger.warning(
                "GetCdrByUniqueIdQuery: "
                f"Unable to connect to database with CDR. {e}"
            )
            raise e

        cur = await conn.cursor()
        await cur.execute(
            f"SELECT calldate, recordingfile "
            f"FROM cdr WHERE uniqueid={unique_id}"
        )
        try:
            date, filename = await cur.fetchone()
        except TypeError:
            raise FileNotFoundError(
                f"File with unique_id: `{unique_id}` not found."
            )
        await cur.close()
        conn.close()

        if not date or not filename:
            raise FileNotFoundError(
                f"File with unique_id: `{unique_id}` not found."
            )

        extension = filename.split(".")[-1]

        parent_path = date.strftime(self.__config.media_root).rstrip('/')
        if not os.path.exists(parent_path):
            await self.__logger.warning(
                "GetCdrByUniqueIdQuery: "
                f"There is no such media_root: '{parent_path}'. "
                f"Check config."
            )
            raise FileNotFoundError()

        full_path = os.path.join(
            parent_path,
            filename,
        )

        if not os.path.exists(full_path):
            raise FileNotFoundError(
                f"File with unique_id: `{unique_id}` "
                f"path: `{full_path}` not found."
            )

        content = await self.__get_content_from_file(full_path)

        if extension == "mp3":
            filetype = Filetype.MP3
        elif extension == "mp4":
            filetype = Filetype.MP3
        elif extension == "wav":
            filetype = Filetype.WAV
        elif extension == "WAV":
            filetype = Filetype.WAV
        elif extension == "WAVE":
            filetype = Filetype.WAVE
        else:
            raise Exception(
                "Unknown file extension."
            )

        return File(
            name=filename,
            type=filetype,
            content=content,
        )

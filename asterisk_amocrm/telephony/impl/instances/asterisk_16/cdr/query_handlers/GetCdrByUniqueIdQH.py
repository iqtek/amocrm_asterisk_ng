import os

import aiofiles
from pydub import AudioSegment

from asterisk_amocrm.domains import GetCdrByUniqueIdQuery, IGetCdrByUniqueIdQH
from asterisk_amocrm.domains.models import File, Filetype
from asterisk_amocrm.infrastructure import ILogger
from ..CdrProviderConfig import CdrProviderConfig
from ..mysql import MySqlConnectionFactoryImpl


__all__ = [
    "GetCdrByUniqueIdQH",
]


class GetCdrByUniqueIdQH(IGetCdrByUniqueIdQH):

    def __init__(
        self,
        config: CdrProviderConfig,
        mysql_connection_factory: MySqlConnectionFactoryImpl,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__mysql_connection_factory = mysql_connection_factory
        self.__logger = logger

    async def __get_content_from_file(
        self,
        path: str
    ) -> bytes:
        async with aiofiles.open(
            path,
            mode='rb',
        ) as f:
            content = await f.read()
        return content

    async def __get_existing_mp3_file(
        self,
        filename_without_ext: str,
        main_path: str,
        tmp_path: str,
    ) -> File:
        filename = filename_without_ext + ".mp3"
        self.__logger.debug(
            f"GetCdrByUniqueIdQH: attempt of get {filename}"
        )
        main_full_path = os.path.join(
            main_path,
            filename,
        )
        tmp_full_path = os.path.join(
            tmp_path,
            filename,
        )
        if os.path.exists(main_full_path):
            content = await self.__get_content_from_file(main_full_path)
            file = File(
                name=filename,
                type=Filetype.MP3,
                content=content
            )
            self.__logger.debug(
                "GetCdrByUniqueIdQH: "
                f"file {filename} found in main repository."
            )
            return file

        elif os.path.exists(tmp_full_path):
            content = await self.__get_content_from_file(tmp_full_path)
            file = File(
                name=filename,
                type=Filetype.MP3,
                content=content
            )
            self.__logger.debug(
                "GetCdrByUniqueIdQH: "
                f"file {filename} in tmp repository."
            )
            return file
        else:
            raise FileNotFoundError(filename)

    def __wav_to_mp3_convert(
        self,
        main_path: str,
        filename_without_ext: str,
        tmp_directory: str,
    ) -> None:
        audio = AudioSegment.from_wav(
            f"{main_path}/{filename_without_ext}.{self.__config.wav_extension}"
        )
        audio.export(
            f"{tmp_directory}/{filename_without_ext}.mp3",
            format='mp3',
            bitrate='16k'
        )

    async def __call__(self, query: GetCdrByUniqueIdQuery) -> File:
        unique_id = query.unique_id
        conn = await self.__mysql_connection_factory.get_instance(
            settings=self.__config.mysql,
        )
        cur = await conn.cursor()
        await cur.execute(
            f"SELECT calldate, recordingfile "
            f"FROM cdr WHERE uniqueid={unique_id}"
        )
        date, filename = await cur.fetchone()
        await cur.close()
        conn.close()
        if not date or not filename:
            raise FileNotFoundError(
                f"File with unique_id: {unique_id} not found."
            )
        filename_without_ext, ext_with_point = os.path.splitext(filename)

        try:
            main_path = date.strftime(self.__config.media_root).rstrip('/')
            tmp_path = date.strftime(self.__config.tmp_media_root).rstrip('/')
        except ValueError:
            self.__logger.warning(
                "GetCdrByUniqueIdQH: "
                "Invalid path mask"
            )
            raise ValueError

        try:
            file = await self.__get_existing_mp3_file(
                filename_without_ext=filename_without_ext,
                main_path=main_path,
                tmp_path=tmp_path,
            )
            return file
        except FileNotFoundError:
            self.__logger.debug(
                "GetCdrByUniqueIdQH: "
                f"The file {filename} is not in any of the repositories."
            )

        if os.path.exists(
            os.path.join(
                main_path,
                f"{filename_without_ext}.{self.__config.wav_extension}",
            )
        ):
            self.__wav_to_mp3_convert(
                main_path=main_path,
                filename_without_ext=filename_without_ext,
                tmp_directory=tmp_path
            )
        else:
            self.__logger.warning(
                "GetCdrByUniqueIdQH: "
                f"The file {main_path}/{filename}."
                f"{self.__config.wav_extension} not found."
            )
            raise FileNotFoundError(
                f"{main_path}{filename}.{self.__config.wav_extension}"
            )
        file = await self.__get_existing_mp3_file(
            filename_without_ext=filename_without_ext,
            main_path=main_path,
            tmp_path=tmp_path,
        )
        return file

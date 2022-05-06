import os

import aiofiles
from pydub import AudioSegment

from amocrm_asterisk_ng.domain import File
from amocrm_asterisk_ng.domain import Filetype

from ..core import IFileConverter
from ...CallRecordsConfig import CallRecordsConfig


__all__ = [
    "PydubFileConverter",
]


class PydubFileConverter(IFileConverter):

    __slots__ = (
        "__config",
    )

    def __init__(
        self,
        config: CallRecordsConfig,
    ) -> None:
        self.__config = config

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

    async def convert(self, file: File, new_filetype: Filetype) -> File:

        if file.type == new_filetype:
            return file

        if not os.path.exists(self.__config.tmp_directory):
            try:
                os.mkdir(self.__config.tmp_directory)
            except Exception as exc:
                raise Exception(
                    "PydubFileConverter: "
                    f"directory: {self.__config.tmp_directory} "
                    f"is missing."
                )

        filepath = os.path.join(
            self.__config.tmp_directory,
            file.name,
        )
        async with aiofiles.open(
            filepath,
            mode='wb',
        ) as f:
            await f.write(file.content)

        if file.type == Filetype.MP3:
            audio = AudioSegment.from_mp3(filepath)
        elif file.type == Filetype.WAV:
            audio = AudioSegment.from_wav(filepath)
        elif file.type == Filetype.WAVE:
            audio = AudioSegment.from_WAVE(filepath)
        else:
            raise Exception(
                f"Non-convertible type: {file.type}."
            )

        new_filepath = os.path.join(
            self.__config.tmp_directory,
            "converted_" + file.name,
        )

        if new_filepath == Filetype.MP3:
            new_format = "mp3"
        elif file.type == Filetype.WAV:
            new_format = "wav"
        elif file.type == Filetype.WAVE:
            new_format = "wave"
        else:
            raise Exception(
                f"Non-convertible type: {new_filepath}."
            )
        audio.export(
            new_filepath,
            format=new_format,
            bitrate='16k'
        )

        content = await self.__get_content_from_file(new_filepath)

        os.remove(filepath)
        os.remove(new_filepath)

        return File(
            name=file.name,
            type=Filetype.MP3,
            content=content,
        )

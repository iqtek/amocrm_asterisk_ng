import os
from time import time

import aiofiles
from pydub import AudioSegment

from asterisk_ng.interfaces import File
from asterisk_ng.interfaces import Filetype

from ..core import FileConverterException
from ..core import IFileConverter


__all__ = ["FileConverterImpl"]


class FileConverterImpl(IFileConverter):

    __slots__ = (
        "__tmp_directory",
    )

    def __init__(self, tmp_dir: str) -> None:
        self.__tmp_directory = tmp_dir

    async def __get_content_from_file(self, path: str) -> bytes:
        async with aiofiles.open(path, mode='rb') as f:
            content = await f.read()
        return content

    async def convert(self, file: File, new_filetype: Filetype) -> File:

        if file.type == new_filetype:
            return file

        if not os.path.exists(self.__tmp_directory):
            try:
                os.makedirs(self.__tmp_directory)
            except OSError as exc:
                raise FileConverterException(
                    f"Error creating temporary directory."
                ) from exc

        unique_id = str(time())

        filepath = os.path.join(self.__tmp_directory, file.name + unique_id)
        
        async with aiofiles.open(filepath, mode='wb') as f:
            await f.write(file.content)

        if file.type == Filetype.MP3:
            audio = AudioSegment.from_mp3(filepath)
        elif file.type == Filetype.WAV:
            audio = AudioSegment.from_wav(filepath)
        elif file.type == Filetype.WAVE:
            audio = AudioSegment.from_wav(filepath)
        else:
            raise FileConverterException(f"Non-convertible filetype: `{file.type}`.")

        new_filepath = os.path.join(
            self.__tmp_directory,
            "converted_" + file.name + unique_id,
        )

        if new_filetype == Filetype.MP3:
            new_format = "mp3"
        elif new_filetype == Filetype.WAV:
            new_format = "wav"
        elif new_filetype == Filetype.WAVE:
            new_format = "wave"
        else:
            raise FileConverterException(f"Non-convertible filetype: `{file.type}`.")

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
            type=new_filetype,
            content=content,
        )

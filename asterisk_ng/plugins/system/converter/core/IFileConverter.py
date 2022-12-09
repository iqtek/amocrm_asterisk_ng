from asterisk_ng.interfaces import File
from asterisk_ng.interfaces import Filetype


__all__ = ["IFileConverter"]


class IFileConverter:

    __slots__ = ()

    async def convert(self, file: File, new_filetype: Filetype) -> File:
        raise NotImplementedError()

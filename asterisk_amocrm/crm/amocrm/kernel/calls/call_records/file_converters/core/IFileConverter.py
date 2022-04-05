from asterisk_amocrm.domains import File
from asterisk_amocrm.domains import Filetype


__all__ = [
    "IFileConverter",
]


class IFileConverter:

    __slots__ = ()

    async def convert(self, file: File, new_filetype: Filetype) -> File:
        raise NotImplementedError()

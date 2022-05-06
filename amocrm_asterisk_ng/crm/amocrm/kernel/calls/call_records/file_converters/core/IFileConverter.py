from amocrm_asterisk_ng.domain import File
from amocrm_asterisk_ng.domain import Filetype


__all__ = [
    "IFileConverter",
]


class IFileConverter:

    __slots__ = ()

    async def convert(self, file: File, new_filetype: Filetype) -> File:
        raise NotImplementedError()

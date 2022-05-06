from .Filetype import Filetype


__all__ = [
    "File",
]


class File:

    __slots__ = (
        "__type",
        "__name",
        "__content",
    )

    def __init__(
        self,
        name: str,
        type: Filetype,
        content: bytes
    ) -> None:
        self.__name = name
        self.__type = type
        self.__content = content

    @property
    def name(self) -> str:
        return self.__name

    @property
    def type(self) -> Filetype:
        return self.__type

    @property
    def content(self) -> bytes:
        return self.__content

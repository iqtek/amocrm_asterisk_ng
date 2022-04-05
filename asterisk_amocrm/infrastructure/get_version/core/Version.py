__all__ = [
    "Version",
]


class Version:

    __slots__ = (
        "__major",
        "__minor",
        "__micro",
    )

    def __init__(
        self,
        major: int,
        minor: int,
        micro: int,
    ) -> None:
        self.__major = major
        self.__minor = minor
        self.__micro = micro

    @property
    def major(self) -> int:
        return self.__major

    @property
    def minor(self) -> int:
        return self.__minor

    @property
    def micro(self) -> int:
        return self.__micro

    def __repr__(self) -> str:
        return f"{self.__major}.{self.__minor}.{self.__micro}"

from ..core import Version
from ..core import IGetCurrentAppVersionFunction


__all__ = [
    "GetCurrentAppVersionFunction",
]


class GetCurrentAppVersionFunction(IGetCurrentAppVersionFunction):

    __slots__ = (
        "__current_app_version",
    )

    def __init__(
        self,
        current_app_version: Version,
    ) -> None:
        self.__current_app_version = current_app_version

    def __call__(self) -> Version:
        return self.__current_app_version

from .models import DynamicConfiguration
from .models import StaticConfiguration


__all__ = ["IConfigurator"]


class IConfigurator:

    __slots__ = ()

    async def get_static_configuration(self) -> StaticConfiguration:
        raise NotImplementedError()

    async def set_configuration(self, configuration: DynamicConfiguration) -> None:
        raise NotImplementedError()

    async def get_configuration(self) -> DynamicConfiguration:
        raise NotImplementedError()

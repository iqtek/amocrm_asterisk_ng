from asyncio import get_running_loop
from typing import Any
from typing import Mapping
from typing import Optional

from .Integration import Integration
from .IntegrationFactory import IntegrationFactory


__all__ = [
    "IntegrationLauncher",
]


class IntegrationLauncher:

    __slots__ = (
        "__integration_factory",
        "__integration",
        "__settings",
    )

    def __init__(
        self,
        integration_factory: IntegrationFactory,
        settings: Mapping[str, Any]
    ) -> None:
        self.__integration_factory = integration_factory
        self.__settings = settings
        self.__integration: Optional[Integration] = None

    async def handle_startup(self) -> None:
        event_loop = get_running_loop()
        self.__integration = self.__integration_factory.get_instance(
            settings=self.__settings,
            event_loop=event_loop,
        )
        await self.__integration.handle_startup()

    async def handle_shutdown(self) -> None:
        await self.__integration.handle_shutdown()

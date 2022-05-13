from typing import Optional

from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import InitializableComponent

from ....core import IAmiManager


__all__ = [
    "Asterisk16Component",
]


class Asterisk16Component(AbstractInitializableComponent):

    __slots__ = (
        "__ami_manager",
        "__ami_component",
        "__cdr_component",
        "__origination_component",
        "__storage",
    )

    def __init__(
        self,
        ami_manager: IAmiManager,
        cdr_component: InitializableComponent,
        origination_component: InitializableComponent,
        storage: InitializableComponent,
    ) -> None:
        super().__init__()
        self.__ami_manager = ami_manager
        self.__cdr_component = cdr_component
        self.__origination_component = origination_component
        self.__storage = storage

    async def _initialize(self) -> None:
        await self.__storage.initialize()
        await self.__ami_manager.connect()
        await self.__cdr_component.initialize()
        await self.__origination_component.initialize()

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        await self.__cdr_component.deinitialize()
        await self.__origination_component.deinitialize()
        self.__ami_manager.disconnect()
        await self.__storage.deinitialize()

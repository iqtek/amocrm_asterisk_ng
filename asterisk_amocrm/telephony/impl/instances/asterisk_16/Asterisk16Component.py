from asterisk_amocrm.infrastructure import InitializableComponent
from asterisk_amocrm.infrastructure import ILogger

from ....core import IAmiManager


__all__ = [
    "Asterisk16Component",
]


class Asterisk16Component(InitializableComponent):

    __slots__ = (
        "__ami_manager",
        "__ami_component",
        "__cdr_component",
        "__origination_component",
    )

    def __init__(
        self,
        ami_manager: IAmiManager,
        ami_component: InitializableComponent,
        cdr_component: InitializableComponent,
        origination_component: InitializableComponent,
    ) -> None:
        self.__ami_manager = ami_manager
        self.__ami_component = ami_component
        self.__cdr_component = cdr_component
        self.__origination_component = origination_component

    async def initialize(self):
        await self.__ami_manager.connect()
        await self.__ami_component.initialize()
        await self.__cdr_component.initialize()
        await self.__origination_component.initialize()

    async def deinitialize(self):
        self.__ami_manager.disconnect()
        await self.__ami_component.deinitialize()
        await self.__cdr_component.deinitialize()
        await self.__origination_component.deinitialize()

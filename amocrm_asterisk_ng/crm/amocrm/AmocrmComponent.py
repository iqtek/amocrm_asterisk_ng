from typing import Optional

from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import InitializableComponent


__all__ = [
    "AmocrmComponent",
]


class AmocrmComponent(AbstractInitializableComponent):

    __slots__ = (
        "__amocrm_kernel_component",
        "__widget_component",
    )

    def __init__(
        self,
        widget_component: InitializableComponent,
        amocrm_kernel_component: InitializableComponent,
    ) -> None:
        super().__init__()
        self.__amocrm_kernel_component = amocrm_kernel_component
        self.__widget_component = widget_component

    async def _initialize(self) -> None:
        await self.__widget_component.initialize()
        await self.__amocrm_kernel_component.initialize()

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        await self.__widget_component.deinitialize()
        await self.__amocrm_kernel_component.deinitialize()

from asterisk_amocrm.infrastructure import (
    IComponent,
)


__all__ = [
    "AmocrmComponent",
]


class AmocrmComponent(IComponent):

    def __init__(
        self,
        widget_component: IComponent,
        amocrm_kernel_component: IComponent,
    ) -> None:
        self.__amocrm_kernel_component = amocrm_kernel_component
        self.__widget_component = widget_component

    async def initialize(self) -> None:
        await self.__widget_component.initialize()
        await self.__amocrm_kernel_component.initialize()

    async def deinitialize(self) -> None:
        await self.__widget_component.deinitialize()
        await self.__amocrm_kernel_component.deinitialize()

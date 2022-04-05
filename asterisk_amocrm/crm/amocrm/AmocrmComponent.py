from asterisk_amocrm.infrastructure import InitializableComponent


__all__ = [
    "AmocrmComponent",
]


class AmocrmComponent(InitializableComponent):

    __slots__ = (
        "__amocrm_kernel_component",
        "__widget_component",
    )

    def __init__(
        self,
        widget_component: InitializableComponent,
        amocrm_kernel_component: InitializableComponent,
    ) -> None:
        self.__amocrm_kernel_component = amocrm_kernel_component
        self.__widget_component = widget_component

    async def initialize(self) -> None:
        await self.__widget_component.initialize()
        await self.__amocrm_kernel_component.initialize()

    async def deinitialize(self) -> None:
        await self.__widget_component.deinitialize()
        await self.__amocrm_kernel_component.deinitialize()

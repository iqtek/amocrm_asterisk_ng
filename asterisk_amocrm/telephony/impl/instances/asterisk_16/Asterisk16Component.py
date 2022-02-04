from asterisk_amocrm.infrastructure import IComponent, ILogger


__all__ = [
    "Asterisk16Component",
]


class Asterisk16Component(IComponent):

    def __init__(
        self,
        ami_component: IComponent,
        cdr_component: IComponent,
        origination_component: IComponent,
        logger: ILogger,
    ) -> None:
        self.__ami_component = ami_component
        self.__cdr_component = cdr_component
        self.__origination_component = origination_component
        self.__logger = logger

    async def initialize(self):
        self.__logger.debug("Asterisk16Component start of initialization.")
        await self.__ami_component.initialize()
        await self.__cdr_component.initialize()
        await self.__origination_component.initialize()
        self.__logger.debug("Asterisk16Component: initialized.")

    async def deinitialize(self):
        self.__logger.debug("Asterisk16Component start of deinitialization.")
        await self.__ami_component.deinitialize()
        await self.__cdr_component.deinitialize()
        await self.__origination_component.deinitialize()
        self.__logger.debug("Asterisk16Component: deinitialized!")

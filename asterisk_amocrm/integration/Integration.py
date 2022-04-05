from typing import Collection

from asterisk_amocrm.infrastructure import InitializableComponent
from asterisk_amocrm.infrastructure import ILogger


__all__ = [
    "Integration",
]


class Integration:

    __slots__ = (
        "__components",
        "__logger",
    )

    def __init__(
        self,
        components: Collection[InitializableComponent],
        logger: ILogger,
    ) -> None:
        self.__components: Collection[InitializableComponent] = components
        self.__logger = logger

    async def handle_startup(self) -> None:
        self.__logger.info("Integration initialization started.")
        for component in self.__components:
            component_name = component.__class__.__name__
            self.__logger.info(
                f"Component initialization: {component_name}."
            )
            try:
                await component.initialize()
            except Exception as e:
                self.__logger.critical(
                    f"Error of initialization: {component_name}. {e}"
                )
                raise Exception("Error of initialization.") from e
        self.__logger.info("Integration initialization finished.")

    async def handle_shutdown(self) -> None:
        self.__logger.info("Integration deinitialization started.")
        for component in self.__components:
            component_name = component.__class__.__name__
            self.__logger.info(
                f"Component deinitialization: {component_name}."
            )
            try:
                await component.deinitialize()
            except Exception as e:
                self.__logger.critical(
                    f"Error of deinitialization: {component_name}. {e}"
                )
                raise Exception("Error of deinitialization.") from e
        self.__logger.info("Integration deinitialization finished.")

from typing import Collection
from typing import Sequence

from glassio.logger import InitializableLogger
from glassio.initializable_components import InitializableComponent
from amocrm_asterisk_ng.scenario import IScenario


__all__ = [
    "Integration",
]


class Integration:

    __slots__ = (
        "__scenario",
        "__listening_components",
        "__control_components",
        "__infrastructure_components",
        "__logger",
    )

    def __init__(
        self,
        scenario: IScenario,
        listening_components: Collection[InitializableComponent],
        control_components: Collection[InitializableComponent],
        infrastructure_components: Sequence[InitializableComponent],
        logger: InitializableLogger,
    ) -> None:
        self.__scenario = scenario
        self.__listening_components = listening_components
        self.__control_components = control_components
        self.__infrastructure_components = infrastructure_components
        self.__logger = logger

    async def __initialize_component(
        self,
        component: InitializableComponent,
    ) -> None:
        component_name = component.__class__.__name__
        try:
            await component.initialize()
        except Exception as e:
            await self.__logger.critical(
                f"Error of initialization: `{component_name}`. {e!r}"
            )
            raise Exception("Error of initialization.") from e
        await self.__logger.info(
            f"Component: `{component_name}` initialized."
        )

    async def __deinitialize_component(
        self,
        component: InitializableComponent,
    ) -> None:
        component_name = component.__class__.__name__
        try:
            await component.deinitialize()
        except Exception as e:
            await self.__logger.critical(
                f"Error of deinitialization: `{component_name}`. {e!r}"
            )
            raise Exception("Error of initialization.") from e

        await self.__logger.info(
            f"Component: `{component_name}` deinitialized."
        )

    async def handle_startup(self) -> None:
        await self.__logger.initialize()
        await self.__logger.info("Integration initialization started.")

        for component in self.__infrastructure_components:
            await self.__initialize_component(component)

        for component in self.__control_components:
            await self.__initialize_component(component)

        for component in self.__listening_components:
            await self.__initialize_component(component)

        await self.__scenario.upload()
        await self.__logger.info("Integration initialization finished.")

    async def handle_shutdown(self) -> None:
        await self.__logger.info("Integration deinitialization started.")

        for component in self.__listening_components:
            await self.__deinitialize_component(component)

        for component in reversed(self.__infrastructure_components):
            await self.__deinitialize_component(component)

        for component in self.__control_components:
            await self.__deinitialize_component(component)

        await self.__scenario.unload()

        await self.__logger.info("Integration deinitialization finished.")
        await self.__logger.deinitialize()

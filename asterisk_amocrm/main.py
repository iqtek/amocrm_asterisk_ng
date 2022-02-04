from asyncio import (
    AbstractEventLoop,
    get_event_loop,
)
from typing import (
    Optional,
    Mapping,
    Any,
)
from fastapi import FastAPI
from uvicorn import run
from asterisk_amocrm.infrastructure import (
    IComponent,
    logger_startup,
    storage_startup,
    dispatcher_startup,
    event_bus_startup,
)
from asterisk_amocrm.telephony import telephony_startup
from asterisk_amocrm.crm import crm_startup
from .IntegrationConfigModel import IntegrationConfigModel


class Integration:

    def __init__(self, settings: Mapping[str, Any]) -> None:
        self.__app = FastAPI()
        self.__settings = settings
        self.__logger = logger_startup(
            settings=settings["infrastructure"]["logging"]
        )
        self.__dispatcher = dispatcher_startup(logger=self.__logger)
        self.__event_bus = event_bus_startup(logger=self.__logger)
        self.__storage = storage_startup(
            logger=self.__logger,
            settings=settings["infrastructure"]["storage"]
        )
        self.__crm: IComponent
        self.__event_loop: Optional[AbstractEventLoop] = None

    async def __handle_startup(self) -> None:
        self.__event_loop = get_event_loop()

        self.__crm = crm_startup(
            settings=self.__settings["crm"],
            app=self.__app,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
            storage=self.__storage.get_instance("amocrm"),
            logger=self.__logger,
        )

        self.__telephony = telephony_startup(
            settings=self.__settings["telephony"],
            dispatcher=self.__dispatcher,
            event_bus=self.__event_bus,
            event_loop=self.__event_loop,
            logger=self.__logger,
            storage=self.__storage.get_instance("telephony"),
        )
        await self.__telephony.initialize()
        await self.__crm.initialize()

    async def __handle_shutdown(self) -> None:
        await self.__crm.deinitialize()
        await self.__telephony.deinitialize()

    def startup(self) -> None:

        self.__app.add_event_handler("startup", self.__handle_startup)
        self.__app.add_event_handler("shutdown", self.__handle_shutdown)

        integration_config = IntegrationConfigModel(
            **self.__settings["infrastructure"]["integration"]
        )
        run(
            self.__app,
            host=integration_config.host,
            port=integration_config.port,
            loop="asyncio",
        )

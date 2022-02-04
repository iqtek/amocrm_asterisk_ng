from asyncio import AbstractEventLoop
from typing import Any, Mapping

from asterisk_amocrm.infrastructure import (
    IComponent,
    IDispatcher,
    IEventBus,
    IFactory,
    IKeyValueStorage,
    ILogger,
)
from .ami import AmiComponentFactory
from .ami_convert_function import AmiMessageConvertFunctionImpl
from .Asterisk16Component import Asterisk16Component
from .Asterisk16Config import Asterisk16Config
from .cdr import CdrProviderComponentFactory
from .origination import OriginationComponentFactory
from ...ami_manager import AmiManagerFactory


__all__ = [
    "Asterisk16ComponentFactory",
]


class Asterisk16ComponentFactory(IFactory):

    def __init__(
        self,
        dispatcher: IDispatcher,
        event_bus: IEventBus,
        storage: IKeyValueStorage,
        event_loop: AbstractEventLoop,
        logger: ILogger,
    ) -> None:
        self.__dispatcher = dispatcher
        self.__event_bus = event_bus
        self.__storage = storage
        self.__event_loop = event_loop
        self.__logger = logger

    @classmethod
    def type(cls):
        return "asterisk_16"

    def get_instance(
        self,
        settings: Mapping[str, Any]
    ) -> IComponent:
        config = Asterisk16Config(**settings)

        ami_message_convert_function = AmiMessageConvertFunctionImpl()

        ami_manager_factory = AmiManagerFactory(
            event_loop=self.__event_loop,
            ami_message_convert_function=ami_message_convert_function,
            logger=self.__logger
        )

        ami_manager = ami_manager_factory.get_instance(
            settings=config.ami,
        )

        ami_component_factory = AmiComponentFactory(
            ami_manager=ami_manager,
            storage=self.__storage,
            event_bus=self.__event_bus,
            event_loop=self.__event_loop,
            logger=self.__logger,
        )
        ami_component = ami_component_factory.get_instance()

        cdr_component_factory = CdrProviderComponentFactory(
            dispatcher=self.__dispatcher,
            event_loop=self.__event_loop,
            logger=self.__logger,
        )
        cdr_component = cdr_component_factory.get_instance(config.cdr)

        origination_component_factory = OriginationComponentFactory(
            ami_manager=ami_manager,
            event_bus=self.__event_bus,
            dispatcher=self.__dispatcher,
        )
        origination_component = origination_component_factory.get_instance(
            config.dial
        )
        telephony_component = Asterisk16Component(
            ami_component=ami_component,
            cdr_component=cdr_component,
            origination_component=origination_component,
            logger=self.__logger,
        )
        return telephony_component

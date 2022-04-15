from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.infrastructure import IKeyValueStorageFactory
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import InitializableComponent
from amocrm_asterisk_ng.infrastructure import ISelectableFactory
from amocrm_asterisk_ng.infrastructure import ISetContextVarsFunction

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


class Asterisk16ComponentFactory(ISelectableFactory[InitializableComponent]):

    __slots__ = (
        "__dispatcher",
        "__event_bus",
        "__storage_factory",
        "__event_loop",
        "__set_context_vars_function",
        "__logger",
    )

    def __init__(
        self,
        dispatcher: IDispatcher,
        event_bus: IEventBus,
        storage_factory: IKeyValueStorageFactory,
        event_loop: AbstractEventLoop,
        set_context_vars_function: ISetContextVarsFunction,
        logger: ILogger,
    ) -> None:
        self.__dispatcher = dispatcher
        self.__event_bus = event_bus
        self.__storage_factory = storage_factory
        self.__event_loop = event_loop
        self.__set_context_vars_function = set_context_vars_function
        self.__logger = logger

    def unique_tag(self) -> str:
        return "asterisk_16"

    def get_instance(
        self,
        settings: Optional[Mapping[str, Any]] = None,
    ) -> InitializableComponent:

        config = Asterisk16Config(**settings)

        storage = self.__storage_factory.get_instance(
            prefix=config.storage_prefix,
        )

        ami_message_convert_function = AmiMessageConvertFunctionImpl()

        ami_manager_factory = AmiManagerFactory(
            event_loop=self.__event_loop,
            set_context_vars_function=self.__set_context_vars_function,
            ami_message_convert_function=ami_message_convert_function,
            logger=self.__logger
        )

        ami_manager = ami_manager_factory.get_instance(
            settings=config.ami,
        )

        ami_component_factory = AmiComponentFactory(
            ami_manager=ami_manager,
            storage=storage,
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
            ami_manager=ami_manager,
            ami_component=ami_component,
            cdr_component=cdr_component,
            origination_component=origination_component,
        )
        return telephony_component

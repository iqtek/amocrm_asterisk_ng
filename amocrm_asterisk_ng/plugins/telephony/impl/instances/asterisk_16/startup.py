from asyncio import AbstractEventLoop
from typing import Any
from typing import Mapping

from glassio.dispatcher import IDispatcher
from amocrm_asterisk_ng.infrastructure import IKeyValueStorageFactory
from glassio.logger import ILogger
from glassio.event_bus import InitializableEventBus
from amocrm_asterisk_ng.infrastructure import ioc

from .ami_convert_function import AmiMessageConvertFunctionImpl
from .ami_handlers import AmiComponentFactory
from .Asterisk16Component import Asterisk16Component
from .Asterisk16Config import Asterisk16Config
from .cdr_provider import CdrProviderComponentFactory
from .origination import OriginationComponentFactory
from ...ami_manager import AmiManagerFactory


__all__ = [
    "asterisk16_startup",
]


def asterisk16_startup(
    settings: Mapping[str, Any],
) -> None:

    dispatcher = ioc.get_instance(IDispatcher)
    event_bus = ioc.get_instance(InitializableEventBus)
    storage_factory = ioc.get_instance(IKeyValueStorageFactory)
    event_loop = ioc.get_instance(AbstractEventLoop)
    logger = ioc.get_instance(ILogger)
    
    config = Asterisk16Config(**settings)

    storage = storage_factory.get_instance(
        prefix=config.storage_prefix,
    )

    ami_message_convert_function = AmiMessageConvertFunctionImpl()

    ami_manager_factory = AmiManagerFactory(
        event_loop=event_loop,
        ami_message_convert_function=ami_message_convert_function,
        logger=logger
    )

    ami_manager = ami_manager_factory.get_instance(
        settings=config.ami,
    )

    ami_component_factory = AmiComponentFactory(
        ami_manager=ami_manager,
        storage=storage,
        event_bus=event_bus,
        event_loop=event_loop,
        logger=logger,
    )
    ami_component = ami_component_factory.get_instance()

    cdr_component_factory = CdrProviderComponentFactory(
        dispatcher=dispatcher,
        event_loop=event_loop,
        logger=logger,
    )
    cdr_component = cdr_component_factory.get_instance(config.cdr)

    origination_component_factory = OriginationComponentFactory(
        ami_manager=ami_manager,
        dispatcher=dispatcher,
    )
    origination_component = origination_component_factory.get_instance(
        config.dial
    )
    telephony_component = Asterisk16Component(
        ami_manager=ami_manager,
        cdr_component=cdr_component,
        origination_component=origination_component,
        storage=storage,
    )

    listening_components = ioc.get("listening_components")
    control_components = ioc.get("control_components")
    control_components.append(telephony_component)
    listening_components.append(ami_component)

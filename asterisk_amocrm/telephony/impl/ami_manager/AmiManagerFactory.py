from asyncio import AbstractEventLoop
from typing import (
    Mapping,
    Any,
)

from panoramisk import Manager

from asterisk_amocrm.infrastructure import ILogger
from .AmiManagerConfigModel import AmiManagerConfigModel
from .AmiManagerImpl import AmiManagerImpl
from ...core import (
    IAmiMessageConvertFunction,
    IAmiManagerFactory,
    IAmiManager,
)
from asterisk_amocrm.infrastructure import (
    trace_id,
    TraceIdValueFactory,
    AddContextVarFunction,
)

__all__ = [
    "AmiManagerFactory",
]


class AmiManagerFactory(IAmiManagerFactory):

    def __init__(
        self,
        event_loop: AbstractEventLoop,
        ami_message_convert_function: IAmiMessageConvertFunction,
        logger: ILogger,
    ) -> None:
        self.__event_loop = event_loop
        self.__ami_message_convert_function = ami_message_convert_function
        self.__logger = logger

    def get_instance(
        self,
        settings: Mapping[str, Any]
    ) -> IAmiManager:

        config = AmiManagerConfigModel.parse_obj(settings)

        panoramisk_manager = Manager(
            host=config.host,
            port=config.port,
            username=config.user,
            secret=config.secret,
            loop=self.__event_loop,
        )

        value_factory = TraceIdValueFactory()
        add_context_var_function = AddContextVarFunction(
            context_var=trace_id,
            value_factory=value_factory,
        )

        ami_manager = AmiManagerImpl(
            manager=panoramisk_manager,
            ami_message_convert_function=self.__ami_message_convert_function,
            add_context_var_function=add_context_var_function,
            logger=self.__logger,
        )

        return ami_manager

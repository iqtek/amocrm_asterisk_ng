from amocrm_asterisk_ng.domain import IAddCallToAnalyticsCommand
from amocrm_asterisk_ng.domain import IAddCallToUnsortedCommand
from amocrm_asterisk_ng.domain import IGetUserIdByPhoneQuery
from amocrm_asterisk_ng.domain import IOriginationCallCommand
from amocrm_asterisk_ng.domain import IOriginationRequestCommand
from amocrm_asterisk_ng.domain import IsUserPhoneNumerQuery
from amocrm_asterisk_ng.domain import IRaiseCardCommand

from glassio.dispatcher import IDispatcher
from glassio.event_bus import IEventBus
from glassio.logger import ILogger

from .ClassicScenarioConfig import ClassicScenarioConfig
from .event_handlers import CallCompletedEventHandler
from .event_handlers import RingingEventHandler

from .functions import GetCallDirectionFunctionImpl
from .functions import IGetCallDirectionFunction
from .functions import IsInternalNumberFunction
from .functions import IsInternalNumberFunctionImpl
from .functions import OriginationRequestCommandImpl

from ...core import IScenario


__all__ = [
    "ClassicScenario",
]


class ClassicScenario(IScenario):

    __slots__ = (
        "__config",
        "__event_bus",
        "__dispatcher",
        "__logger",
    )

    def __init__(
        self,
        config: ClassicScenarioConfig,
        event_bus: IEventBus,
        dispatcher: IDispatcher,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__event_bus = event_bus
        self.__dispatcher = dispatcher
        self.__logger = logger

    async def upload(self) -> None:

        self.__dispatcher.add_function(
            IOriginationRequestCommand,
            OriginationRequestCommandImpl(
                origination_call_command=self.__dispatcher.get_function(IOriginationCallCommand)
            )
        )

        self.__dispatcher.add_function(
            IsInternalNumberFunction,
            IsInternalNumberFunctionImpl(
                is_user_phone_number=self.__dispatcher.get_function(IsUserPhoneNumerQuery),
                internal_number_pattern=self.__config.internal_number_pattern,
            )
        )

        self.__dispatcher.add_function(
            IGetCallDirectionFunction,
            GetCallDirectionFunctionImpl(
                is_internal_number_function=self.__dispatcher.get_function(IsInternalNumberFunction),
            )
        )

        await self.__event_bus.attach_event_handler(
            CallCompletedEventHandler(
                config=self.__config.call_logging,
                add_call_to_analytics_command=self.__dispatcher.get_function(IAddCallToAnalyticsCommand),
                add_call_to_unsorted_command=self.__dispatcher.get_function(IAddCallToUnsortedCommand),
                get_user_id_by_phone_query=self.__dispatcher.get_function(IGetUserIdByPhoneQuery),
                get_call_direction_function=self.__dispatcher.get_function(IGetCallDirectionFunction),
            )
        )

        await self.__event_bus.attach_event_handler(
            RingingEventHandler(
                get_user_id_by_phone_query=self.__dispatcher.get_function(IGetUserIdByPhoneQuery),
                is_internal_number_function=self.__dispatcher.get_function(IsInternalNumberFunction),
                raise_card_command=self.__dispatcher.get_function(IRaiseCardCommand),
            )
        )

    async def unload(self) -> None:
        await self.__event_bus.detach_event_handler(RingingEventHandler)
        await self.__event_bus.detach_event_handler(CallCompletedEventHandler)

        self.__dispatcher.delete_function(IGetCallDirectionFunction)
        self.__dispatcher.delete_function(IsInternalNumberFunction)
        self.__dispatcher.delete_function(IOriginationRequestCommand)

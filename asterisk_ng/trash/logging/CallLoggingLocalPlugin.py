from typing import Any
from typing import Mapping
from typing import MutableSequence
from typing import Optional

from asterisk_ng.interfaces import IGetCrmUserIdsByEmailQuery
from asterisk_ng.interfaces import ILogCallCrmCommand
from asterisk_ng.interfaces import ISendCallNotificationCommand

from asterisk_ng.system.container import container, Key
from asterisk_ng.system.dispatcher import IDispatcher
from asterisk_ng.system.event_bus import IEventBus, IEventBusSubscription
from asterisk_ng.system.logger import ILogger
from asterisk_ng.system.plugin import AbstractPlugin, Interface, PluginInterface

from .event_handlers import RingingTelephonyEventHandler
from .event_handlers import CallCompletedEventHandler


__all__ = ["CallLoggingLocalPlugin"]


class CallLoggingLocalPlugin(AbstractPlugin):

    __slots__ = (
        "__event_bus",
        "__dispatcher",
        "__subscriptions",
    )

    def __init__(self) -> None:
        self.__dispatcher: Optional[IDispatcher] = None
        self.__event_bus: Optional[IEventBus] = None
        self.__subscriptions: MutableSequence[IEventBusSubscription] = []

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                dispatcher=[IGetCrmUserIdsByEmailQuery, ILogCallCrmCommand],
            )
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:
        self.__event_bus = container.resolve(Key(IEventBus))
        self.__dispatcher = container.resolve(Key(IDispatcher))

        self.__subscriptions.append(
            self.__event_bus.subscribe(CallCompletedEventHandler(
                phone_to_agent_id_mapping=PHONE_TO_AGENT_ID_MAPPING,
                log_call_crm_command=self.__dispatcher.get_function(ILogCallCrmCommand)
            ))
        )

        self.__subscriptions.append(
            self.__event_bus.subscribe(RingingTelephonyEventHandler(
                send_call_notification_command=self.__dispatcher.get_function(ISendCallNotificationCommand),
                phone_to_agent_id_mapping=PHONE_TO_AGENT_ID_MAPPING,
            ))
        )

    async def unload(self) -> None:
        for subscription in self.__subscriptions:
            self.__event_bus.cancel_subscription(subscription)

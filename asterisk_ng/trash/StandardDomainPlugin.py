from typing import Any
from typing import Mapping
from typing import MutableSequence
from typing import Optional

from asterisk_ng.interfaces import CrmUserId, ISendCallNotificationCommand
from asterisk_ng.interfaces import (
    IAwaitAgentCallChangeQuery,
    IGetAgentCallQuery,
    IGetContactByPhoneQuery,
    IGetCrmUserQuery,
    IGetResponsibleUserByPhoneQuery,
    IHangupDomainCommand,
    IHangupTelephonyCommand,
    ILogCallCrmCommand,
    IOriginationDomainCommand,
    IOriginationTelephonyCommand,
    IRedirectDomainCommand,
    IRedirectTelephonyCommand,
    ISetMuteDomainCommand,
    ISetMuteTelephonyCommand,
    IGetAgentCollectionQuery,
)
from asterisk_ng.interfaces import IGetCrmUserIdByPhoneQuery, IGetCrmUsersByEmailsQuery
from asterisk_ng.system.container import container, Key
from asterisk_ng.system.dispatcher import IDispatcher
from asterisk_ng.system.event_bus import IEventBus, IEventBusSubscription
from asterisk_ng.system.plugin import AbstractPlugin, Interface, PluginInterface
from .agents.event_handlers import (
    CallCompletedTelephonyEventHandler,
    CallCreatedEventHandler,
    MuteStatusUpdateTelephonyEventHandler,
    RingingTelephonyEventHandler,
)
from .functions import GetCrmUserIdByPhoneQueryImpl
from .logging import CallCompletedEventHandler
from .StandardDomainConfig import StandardDomainConfig


__all__ = [
    "StandardDomainPlugin",
]


class StandardDomainPlugin(AbstractPlugin):

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
                dispatcher=[
                    IGetCrmUsersByEmailsQuery,
                    ILogCallCrmCommand
                ],
            ),
            exported=Interface(
                dispatcher=[
                    IGetCrmUserIdByPhoneQuery,
                    IGetPhoneByCrmUserIdQuery,
                    IGetResponsibleUserByPhoneQuery,
                    IGetAgentCollectionQuery,
                ]
            )
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:
        config = StandardDomainConfig(**settings)
        pass

    async def unload(self) -> None:
        pass

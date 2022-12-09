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
from asterisk_ng.interfaces import IGetCrmUserIdByPhoneQuery, IGetCrmUserIdsByEmailQuery
from asterisk_ng.system.container import container, Key
from asterisk_ng.system.dispatcher import IDispatcher
from asterisk_ng.system.event_bus import IEventBus, IEventBusSubscription
from asterisk_ng.system.logger import ILogger
from asterisk_ng.system.plugin import AbstractPlugin, Interface, PluginInterface
from .agents.event_handlers import (
    CallCompletedTelephonyEventHandler,
    CallCreatedEventHandler,
    MuteStatusUpdateTelephonyEventHandler,
    RingingTelephonyEventHandler,
)
from .functions import (
    AwaitAgentCallChangeQueryImpl,
    GetAgentCallQueryImpl,
    GetResponsibleUserByPhoneQueryImpl,
    HangupDomainCommandImpl,
    OriginationDomainCommandImpl,
    RedirectDomainCommandImpl,
    SetMuteDomainCommandImpl,
    GetAgentCollectionQueryImpl,
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
                dispatcher=[IGetCrmUserIdsByEmailQuery, ILogCallCrmCommand],
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

        self.__event_bus = container.resolve(Key(IEventBus))
        self.__dispatcher = container.resolve(Key(IDispatcher))
        logger = container.resolve(Key(ILogger))

        get_crm_user_ids_by_email_query = self.__dispatcher.get_function(IGetCrmUserIdsByEmailQuery)
        user_ids = await get_crm_user_ids_by_email_query(config.agents.keys())

        # Bijective mapping

        PHONE_TO_AGENT_ID_MAPPING: Mapping[str, CrmUserId] = {
            config.agents[email]: user_ids[email] for email in list(config.agents.keys())
        }

        default_responsible = user_ids.get(config.responsible_agent, None)

        AGENT_ID_TO_PHONE_MAPPING: Mapping[CrmUserId, str] = {v: k for k, v in PHONE_TO_AGENT_ID_MAPPING.items()}

        await_agent_status_change_query = AwaitAgentCallChangeQueryImpl()

        from collections import UserDict

        class Dic(UserDict):

            def __setitem__(self, key, value):
                self.data[key] = value
                await_agent_status_change_query.set_agents_status(key, value)

            def __delitem__(self, key):
                self.data.pop(key)
                await_agent_status_change_query.pop_agents_status(key)

        ACTIVE_CALLS = Dic()

        self.__dispatcher.add_function(
            IAwaitAgentCallChangeQuery,
            await_agent_status_change_query,
        )

        self.__dispatcher.add_function(
            IGetAgentCallQuery,
            GetAgentCallQueryImpl(ACTIVE_CALLS),
        )

        self.__event_bus.subscribe(MuteStatusUpdateTelephonyEventHandler(
            active_calls=ACTIVE_CALLS,
            phone_to_agent_id_mapping=PHONE_TO_AGENT_ID_MAPPING,
        ))

        self.__dispatcher.add_function(
            IGetCrmUserIdByPhoneQuery,
            GetCrmUserIdByPhoneQueryImpl(user_phones=PHONE_TO_AGENT_ID_MAPPING),
        )

        self.__dispatcher.add_function(
            ISetMuteDomainCommand,
            SetMuteDomainCommandImpl(
                agent_id_to_phone_mapping=AGENT_ID_TO_PHONE_MAPPING,
                set_mute_telephony_command=self.__dispatcher.get_function(ISetMuteTelephonyCommand),
            )
        )

        self.__dispatcher.add_function(
            IOriginationDomainCommand,
            OriginationDomainCommandImpl(
                agent_id_to_phone_mapping=AGENT_ID_TO_PHONE_MAPPING,
                origination_telephony_command=self.__dispatcher.get_function(IOriginationTelephonyCommand),
            )
        )

        self.__dispatcher.add_function(
            IRedirectDomainCommand,
            RedirectDomainCommandImpl(
                active_calls=ACTIVE_CALLS,
                redirect_telephony_command=self.__dispatcher.get_function(IRedirectTelephonyCommand),
            )
        )

        self.__dispatcher.add_function(
            IHangupDomainCommand,
            HangupDomainCommandImpl(
                agent_id_to_phone_mapping=AGENT_ID_TO_PHONE_MAPPING,
                hangup_telephony_command=self.__dispatcher.get_function(IHangupTelephonyCommand),
            )
        )

        self.__dispatcher.add_function(
            IGetAgentCollectionQuery,
            GetAgentCollectionQueryImpl(
                agent_id_to_phone_mapping=AGENT_ID_TO_PHONE_MAPPING,
            )
        )

        self.__dispatcher.add_function(
            IGetResponsibleUserByPhoneQuery,
            GetResponsibleUserByPhoneQueryImpl(
                agent_id_to_phone_mapping=AGENT_ID_TO_PHONE_MAPPING,
                get_contact_by_phone_query=self.__dispatcher.get_function(IGetContactByPhoneQuery),
                default_responsible=default_responsible,
            )
        )

        self.__subscriptions.append(
            self.__event_bus.subscribe(
                CallCreatedEventHandler(
                    active_calls=ACTIVE_CALLS,
                    phone_to_agent_id_mapping=PHONE_TO_AGENT_ID_MAPPING,
                    get_contact_by_phone_query=self.__dispatcher.get_function(IGetContactByPhoneQuery),
                    get_crm_user_query=self.__dispatcher.get_function(IGetCrmUserQuery),
                )
            )
        )

        self.__subscriptions.append(
            self.__event_bus.subscribe(CallCompletedTelephonyEventHandler(
                active_calls=ACTIVE_CALLS,
                phone_to_agent_id_mapping=PHONE_TO_AGENT_ID_MAPPING,
            ))
        )

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

        self.__dispatcher.delete_function(IGetCrmUserIdByPhoneQuery)
        self.__dispatcher.delete_function(IHangupDomainCommand)
        self.__dispatcher.delete_function(IOriginationDomainCommand)
        self.__dispatcher.delete_function(ISetMuteDomainCommand)
        self.__dispatcher.delete_function(IRedirectDomainCommand)
        self.__dispatcher.delete_function(IGetAgentCallQuery)

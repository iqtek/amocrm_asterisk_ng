from typing import Any
from typing import Mapping
from typing import MutableSequence
from typing import Optional
from collections import UserDict

from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import Agent

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
    ISendCallNotificationCommand,
    IGetCrmUserIdByPhoneQuery,
    IGetCrmUsersByEmailsQuery,
)

from asterisk_ng.system.container import container, Key
from asterisk_ng.system.dispatcher import IDispatcher
from asterisk_ng.system.event_bus import IEventBus, IEventBusSubscription
from asterisk_ng.system.logger import ILogger
from asterisk_ng.system.plugin import AbstractPlugin, Interface, PluginInterface

from .agents.event_handlers import (
    CallCompletedTelephonyEventHandler,
    CallCreatedEventHandler,
    MuteStatusUpdateTelephonyEventHandler,
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
    GetCrmUserIdByPhoneQueryImpl,
)

from .logging import (
    RingingTelephonyEventHandler,
    CallCompletedEventHandler,
)

from .StandardDomainConfig import StandardDomainConfig


__all__ = ["StandardDomainPlugin"]


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
                dispatcher=[IGetCrmUserByEmailsQuery, ILogCallCrmCommand],
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

        get_crm_users_by_emails_query = self.__dispatcher.get_function(IGetCrmUsersByEmailsQuery)
        crm_users = await get_crm_users_by_emails_query(config.agents.keys())

        AGENTS: Mapping[CrmUserId, Agent] = {
            crm_user.id: Agent(
                user_id=crm_user.id,
                name=crm_user.name,
                phone=config.agents[email],
            )
            for email, crm_user in crm_users.items()
        }
        print("Agents", AGENTS)

        # Bijective mapping
        PHONE_TO_AGENT_MAPPING: Mapping[str, Agent] = {agent.phone: agent for agent in AGENTS.values()}
        AGENT_ID_TO_PHONE_MAPPING: Mapping[CrmUserId, str] = {v.user_id: k for k, v in PHONE_TO_AGENT_MAPPING.items()}

        if responsible_agent_id := crm_users.get(config.responsible_agent, None):
            default_responsible_agent = AGENTS[responsible_agent_id]
        else:
            default_responsible_agent = None

        await_agent_status_change_query = AwaitAgentCallChangeQueryImpl()

        class ProxyActiveCallsDict(UserDict):

            def __setitem__(self, key, value):
                self.data[key] = value
                await_agent_status_change_query.set_agents_status(key, value)

            def __delitem__(self, key):
                self.data.pop(key)
                await_agent_status_change_query.pop_agents_status(key)

        self.__dispatcher.add_function(
            IAwaitAgentCallChangeQuery,
            await_agent_status_change_query,
        )

        ACTIVE_CALLS: [CrmUserId, CallDomainModel] = ProxyActiveCallsDict()

        self.__dispatcher.add_function(
            IGetAgentCallQuery,
            GetAgentCallQueryImpl(ACTIVE_CALLS),
        )

        self.__event_bus.subscribe(
            MuteStatusUpdateTelephonyEventHandler(
                active_calls=ACTIVE_CALLS,
                phone_to_agent_mapping=PHONE_TO_AGENT_MAPPING,
            )
        )

        self.__dispatcher.add_function(
            IGetCrmUserIdByPhoneQuery,
            GetCrmUserIdByPhoneQueryImpl(
                phone_to_agent_mapping=PHONE_TO_AGENT_MAPPING
            )
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
                agents=AGENTS.values(),
            )
        )

        self.__dispatcher.add_function(
            IGetResponsibleUserByPhoneQuery,
            GetResponsibleUserByPhoneQueryImpl(
                agent_id_to_phone_mapping=AGENT_ID_TO_PHONE_MAPPING,
                get_contact_by_phone_query=self.__dispatcher.get_function(IGetContactByPhoneQuery),
                default_responsible=default_responsible_agent,
            )
        )

        self.__subscriptions.append(
            self.__event_bus.subscribe(
                CallCreatedEventHandler(
                    active_calls=ACTIVE_CALLS,
                    phone_to_agent_mapping=PHONE_TO_AGENT_MAPPING,
                    get_contact_by_phone_query=self.__dispatcher.get_function(IGetContactByPhoneQuery),
                    get_crm_user_query=self.__dispatcher.get_function(IGetCrmUserQuery),
                )
            )
        )

        self.__subscriptions.append(
            self.__event_bus.subscribe(
                CallCompletedTelephonyEventHandler(
                    active_calls=ACTIVE_CALLS,
                    phone_to_agent_mapping=PHONE_TO_AGENT_MAPPING,
                )
            )
        )

        # Calls logging and notification.

        self.__subscriptions.append(
            self.__event_bus.subscribe(
                CallCompletedEventHandler(
                    phone_to_agent_mapping=PHONE_TO_AGENT_MAPPING,
                    log_call_crm_command=self.__dispatcher.get_function(ILogCallCrmCommand)
                )
            )
        )

        self.__subscriptions.append(
            self.__event_bus.subscribe(
                RingingTelephonyEventHandler(
                    send_call_notification_command=self.__dispatcher.get_function(ISendCallNotificationCommand),
                    phone_to_agent_mapping=PHONE_TO_AGENT_MAPPING,
                )
            )
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

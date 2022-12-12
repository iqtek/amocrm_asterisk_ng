from typing import Mapping
from typing import MutableMapping
from typing import Optional

from uuid import uuid4
from datetime import datetime
from asterisk_ng.interfaces import CallCreatedTelephonyEvent, CrmUserId, CallDomainModel
from asterisk_ng.interfaces import CallDirection
from asterisk_ng.interfaces import IGetContactByPhoneQuery
from asterisk_ng.system.event_bus import IEventHandler
from asterisk_ng.system.logger import ILogger
from asterisk_ng.interfaces import IGetCrmUserQuery


__all__ = ["CallCreatedEventHandler"]


class CallCreatedEventHandler(IEventHandler):

    __slots__ = (
        "__active_calls",
        "__phone_to_agent_id_mapping",
        "__get_contact_by_phone_query",
        "__get_crm_user_query",
    )

    def __init__(
        self,
        active_calls: MutableMapping[CrmUserId, CallDomainModel],
        phone_to_agent_id_mapping: Mapping[str, CrmUserId],
        get_contact_by_phone_query: IGetContactByPhoneQuery,
        get_crm_user_query: IGetCrmUserQuery,
    ) -> None:
        self.__active_calls = active_calls
        self.__phone_to_agent_id_mapping = phone_to_agent_id_mapping
        self.__get_contact_by_phone_query = get_contact_by_phone_query
        self.__get_crm_user_query = get_crm_user_query

    def __set_call_for_agent(
        self,
        agent_id: CrmUserId,
        client_phone: str,
        direction: CallDirection,
        client_name: Optional[str] = None
    ) -> None:

        call = CallDomainModel(
            id=str(uuid4()),
            agent_id=agent_id,
            client_phone_number=client_phone,
            direction=direction,
            created_at=datetime.now(),
            client_name=client_name,
        )

        self.__active_calls[agent_id] = call

    async def __get_client_name(self, phone: str) -> Optional[str]:
        try:
            contact = await self.__get_contact_by_phone_query(phone)
        except KeyError:
            return None
        return contact.name

    async def __call__(self, event: CallCreatedTelephonyEvent) -> None:

        caller_agent_id = self.__phone_to_agent_id_mapping.get(event.caller_phone_number, None)
        called_agent_id = self.__phone_to_agent_id_mapping.get(event.called_phone_number, None)

        if caller_agent_id is not None and called_agent_id is not None:
            caller_user = await self.__get_crm_user_query(caller_agent_id)
            called_user = await self.__get_crm_user_query(called_agent_id)

            self.__set_call_for_agent(caller_agent_id, event.called_phone_number, CallDirection.INTERNAL, client_name=called_user.name)
            self.__set_call_for_agent(called_agent_id, event.caller_phone_number, CallDirection.INTERNAL, client_name=caller_user.name)
            return

        if caller_agent_id is not None:
            client_name = await self.__get_client_name(event.called_phone_number)
            self.__set_call_for_agent(caller_agent_id, event.called_phone_number, CallDirection.OUTBOUND, client_name=client_name)
            return

        if called_agent_id is not None:
            client_name = await self.__get_client_name(event.caller_phone_number)
            self.__set_call_for_agent(called_agent_id, event.caller_phone_number, CallDirection.INBOUND, client_name=client_name)
            return

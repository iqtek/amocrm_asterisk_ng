from typing import Any
from typing import Mapping
from typing import Optional
from asyncio import wait_for
import asyncio
from asyncio import sleep
from asyncio import CancelledError
from asterisk_ng.interfaces import CrmUserId
from asterisk_ng.interfaces import IAwaitAgentCallChangeQuery
from asterisk_ng.interfaces import IGetAgentCallQuery, CallDomainModel
from ..controller import IControllerMethod
from .models import AgentStatus
from .models import CallStatus
from .models import CallInfo
import asyncio


__all__ = ["GetAgentStatusMethod"]


class GetAgentStatusMethod(IControllerMethod):

    __slots__ = (
        "__get_agent_status_query",
        "__await_agent_status_change_query",
    )

    def __init__(
        self,
        get_agent_status_query: IGetAgentCallQuery,
        await_agent_status_change_query: IAwaitAgentCallChangeQuery,
    ) -> None:
        self.__get_agent_status_query = get_agent_status_query
        self.__await_agent_status_change_query = await_agent_status_change_query

    def __make_conversation_status(self, call: CallDomainModel) -> Mapping[str, Any]:

        if call.contact is not None:
            contact_id = call.contact.id
        else:
            contact_id = None

        return AgentStatus(
            status=CallStatus.CONVERSATION,
            call_info=CallInfo(
                unique_id=call.id,
                contact_phone=call.client_phone_number,
                contact_name=call.client_name,
                contact_id=contact_id,
                is_hold=False,
                is_mute=call.agent_is_mute,
                timestamp=int(call.created_at.timestamp()),
            ),
        ).dict()

    def __make_not_conversation_status(self) -> Mapping[str, Any]:
        return AgentStatus(status=CallStatus.NOT_CONVERSATION).dict()

    async def __call__(
        self,
        amouser_email: str,
        amouser_id: int,
        current_status: Mapping[str, Any] = None,
    ) -> Optional[Mapping[str, Any]]:

        if current_status is None:
            return self.__make_not_conversation_status()

        user_id = CrmUserId(id=amouser_id, email=amouser_email)
        current_agent_status = AgentStatus(**current_status)

        try:
            call_domain_model: CallDomainModel = await self.__get_agent_status_query(user_id)
        except KeyError:
            if current_agent_status.status == CallStatus.CONVERSATION:
                return self.__make_not_conversation_status()
        else:
            if self.__make_conversation_status(call_domain_model) != current_agent_status.dict():
                return self.__make_conversation_status(call_domain_model)

        try:
            call_domain_model: CallDomainModel = await wait_for(
                self.__await_agent_status_change_query(user_id=user_id),
                timeout=9.5,
            )
        except (asyncio.TimeoutError, CancelledError):
            return current_agent_status.dict()
        except KeyError:
            return self.__make_not_conversation_status()

        return self.__make_conversation_status(call_domain_model)

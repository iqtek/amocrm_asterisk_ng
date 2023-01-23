from typing import Any
from typing import Mapping

from fastapi import FastAPI

from asterisk_ng.interfaces import (
    IAwaitAgentCallChangeQuery,
    IGetAgentCallQuery,
    IGetAgentCollectionQuery,
    IHangupDomainCommand,
    IOriginationDomainCommand,
    IRedirectDomainCommand,
    ISetMuteDomainCommand,
)

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key
from asterisk_ng.system.dispatcher import IDispatcher
from asterisk_ng.system.logger import ILogger
from asterisk_ng.system.plugin import AbstractPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface
from .AsteriskNgConfig import AsteriskNgConfig

from .controller import (
    ControllerImpl,
    InvalidMethodParamsException,
    UnknownMethodException,
)

from .fastapi import AuthMiddleware
from .fastapi import bad_request_exception_handler
from .fastapi import BadRequest
from .fastapi import invalid_method_params_exception_handler
from .fastapi import unknown_method_exception_handler

from .methods import GetAgentStatusMethod
from .methods import GetContactsMethod
from .methods import GetLastContactsMethod
from .methods import HangupMethod
from .methods import OriginationByContactMethod
from .methods import OriginationMethod
from .methods import PingMethod
from .methods import RedirectMethod
from .methods import SetMuteMethod
from .methods.models import Contact


__all__ = ["AsteriskNgWidgetPlugin"]


class AsteriskNgWidgetPlugin(AbstractPlugin):

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                container=[
                    Key(FastAPI),
                    Key(ILogger),
                ],
            )
        )

    async def upload(self, settings: Mapping[str, Any]) -> None:

        app = container.resolve(Key(FastAPI))
        dispatcher = container.resolve(Key(IDispatcher))
        logger = container.resolve(Key(ILogger))
        config = AsteriskNgConfig(**settings)

        get_agent_collection_query = dispatcher.get_function(IGetAgentCollectionQuery)

        agents = await get_agent_collection_query()
        contacts = {
            agent.user_id.id:
            Contact(
                uuid=agent.user_id.id,
                name=agent.name,
                phone=agent.phone,
            )
            for agent in agents
        }

        controller = ControllerImpl(logger=logger)

        # Methods

        controller.add_method(
            "ping",
            PingMethod()
        )

        controller.add_method(
            "set_mute",
            SetMuteMethod(
                dispatcher.get_function(ISetMuteDomainCommand)
            )
        )
        controller.add_method(
            "originate",
            OriginationMethod(
                dispatcher.get_function(IOriginationDomainCommand)
            )
        )

        controller.add_method(
            "redirect",
            RedirectMethod(
                dispatcher.get_function(IRedirectDomainCommand)
            )
        )
        controller.add_method(
            "hangup",
            HangupMethod(
                dispatcher.get_function(IHangupDomainCommand)
            )
        )

        controller.add_method(
            "get_agent_status",
            GetAgentStatusMethod(
                get_agent_status_query=dispatcher.get_function(IGetAgentCallQuery),
                await_agent_status_change_query=dispatcher.get_function(IAwaitAgentCallChangeQuery),
            )
        )

        contacts_list = tuple(contacts.values())

        controller.add_method(
            "get_contacts",
            GetContactsMethod(
                contacts=contacts_list,
            )
        )
        controller.add_method(
            "get_last_contacts",
            GetLastContactsMethod(
                contacts=contacts_list,
            )
        )

        controller.add_method(
            "originate_by_contact",
            OriginationByContactMethod(
                contacts=contacts,
                origination_domain_command=dispatcher.get_function(IOriginationDomainCommand),
            )
        )

        app.middleware("http")(AuthMiddleware(secret_key=config.secret_key))
        app.add_api_route("/asterisk_ng", controller.handle, methods=["POST"], tags=["Widgets"])

        app.add_exception_handler(InvalidMethodParamsException, invalid_method_params_exception_handler)
        app.add_exception_handler(UnknownMethodException, unknown_method_exception_handler)
        app.add_exception_handler(BadRequest, bad_request_exception_handler)

    async def unload(self) -> None:
        pass

from typing import Any
from typing import Mapping
from typing import Optional

from amocrm_api_client import AmoCrmApiClient

from asterisk_ng.interfaces import IGetCrmUsersByEmailsQuery
from asterisk_ng.interfaces import IGetContactByPhoneQuery
from asterisk_ng.interfaces import ILogCallCrmCommand
from asterisk_ng.interfaces import ISendCallNotificationCommand
from asterisk_ng.interfaces import IGetCrmUserQuery

from asterisk_ng.plugins.crm_system.amocrm.kernel.records import IGenerateLinkFunction

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key

from asterisk_ng.system.dispatcher import IDispatcher

from asterisk_ng.system.plugin import AbstractPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from .AmocrmFunctionsPluginConfig import AmocrmFunctionsPluginConfig

from .functions import GetCrmUsersByEmailsQueryImpl
from .functions import GetContactByPhoneQueryImpl
from .functions import LogCallCrmCommandImpl
from .functions import SendCallNotificationCommandImpl
from .functions import GetCrmUserQueryImpl

__all__ = ["AmocrmFunctionsPlugin"]


class AmocrmFunctionsPlugin(AbstractPlugin):

    __slots__ = (
        "__dispatcher",
        "__get_crm_user_query_impl",
    )

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                container=[
                    Key(AmoCrmApiClient),
                ],
            ),
            exported=Interface(
                dispatcher=[
                    ISendCallNotificationCommand,
                    IGetCrmUserIdsByEmailQuery,
                    ILogCallCrmCommand,
                    IGetContactByPhoneQuery,
                    IGetCrmUserQuery,
                ]
            )
        )

    def __init__(self) -> None:
        self.__dispatcher: Optional[IDispatcher] = None
        self.__get_crm_user_query_impl: Optional[IGetCrmUserQuery] = None

    async def __get_pipeline_id(
        self,
        amo_client: AmoCrmApiClient,
        pipeline_name: str,
    ) -> int:
        pipelines = await amo_client.pipelines.get_all()

        for pipeline in pipelines:
            if pipeline.name == pipeline_name:
                return pipeline.id

        raise Exception(f"Pipeline: `{pipeline_name}` not found in crm.")

    async def upload(self, settings: Mapping[str, Any]) -> None:

        amo_client = container.resolve(Key(AmoCrmApiClient))
        self.__dispatcher = container.resolve(Key(IDispatcher))

        config = AmocrmFunctionsPluginConfig(**settings)
        pipeline_id = await self.__get_pipeline_id(amo_client, config.pipeline)

        self.__dispatcher.add_function(
            IGetContactByPhoneQuery,
            GetContactByPhoneQueryImpl(
                amo_client=amo_client,
            )
        )

        self.__dispatcher.add_function(
            ISendCallNotificationCommand,
            SendCallNotificationCommandImpl(
                amo_client=amo_client,
            )
        )

        self.__dispatcher.add_function(
            IGetCrmUsersByEmailsQuery,
            GetCrmUsersByEmailsQueryImpl(
                amo_client=amo_client,
            )
        )

        self.__dispatcher.add_function(
            ILogCallCrmCommand,
            LogCallCrmCommandImpl(
                config=config,
                amo_client=amo_client,
                generate_link_function=self.__dispatcher.get_function(IGenerateLinkFunction),
                pipeline_id=pipeline_id,
            )
        )

        self.__get_crm_user_query_impl = GetCrmUserQueryImpl(
            amo_client=amo_client
        )

        await self.__get_crm_user_query_impl.initialize()
        self.__dispatcher.add_function(IGetCrmUserQuery, self.__get_crm_user_query_impl)

    async def unload(self) -> None:
        self.__dispatcher.delete_function(IGetCrmUserQuery)
        await self.__get_crm_user_query_impl.deinitialize()
        self.__dispatcher.delete_function(ISendCallNotificationCommand)
        self.__dispatcher.delete_function(IGetCrmUsersByEmailsQuery)
        self.__dispatcher.delete_function(ILogCallCrmCommand)

from typing import Any
from typing import Mapping
from typing import Optional

from asterisk_ng.system.container import container
from asterisk_ng.system.container import Key

from asterisk_ng.system.dispatcher import IDispatcher
from asterisk_ng.system.plugin import AbstractPlugin
from asterisk_ng.system.plugin import Interface
from asterisk_ng.system.plugin import PluginInterface

from asterisk_ng.interfaces import IGetRecordFileByUniqueIdQuery
from asterisk_ng.system.logger import ILogger
from asterisk_ng.plugins.system.converter import IFileConverter
from fastapi import FastAPI

from .AmocrmRecordsProviderPluginConfig import AmocrmRecordsProviderPluginConfig

from .functions import GenerateLinkFunctionImpl
from .functions import IGenerateLinkFunction
from .CallRecordsView import CallRecordsView


__all__ = ["AmocrmRecordsProviderPlugin"]


class AmocrmRecordsProviderPlugin(AbstractPlugin):

    __slots__ = (
        "__dispatcher",
    )

    @property
    def interface(self) -> PluginInterface:
        return PluginInterface(
            imported=Interface(
                dispatcher=[
                    IGetRecordFileByUniqueIdQuery,
                ],
                container=[
                    Key(FastAPI),
                ]
            ),
            exported=Interface(
                dispatcher=[
                    IGenerateLinkFunction,
                ]
            )
        )

    def __init__(self) -> None:
        self.__dispatcher: Optional[IDispatcher] = None

    async def upload(self, settings: Mapping[str, Any]) -> None:
        self.__dispatcher = container.resolve(Key(IDispatcher))

        file_converter = container.resolve(Key(IFileConverter))
        logger = container.resolve(Key(ILogger))
        config = AmocrmRecordsProviderPluginConfig(**settings)
        app = container.resolve(Key(FastAPI))

        self.__dispatcher.add_function(
            IGenerateLinkFunction,
            GenerateLinkFunctionImpl(base_url=config.base_url)
        )

        call_records_view = CallRecordsView(
            get_record_file_unique_id_query=self.__dispatcher.get_function(IGetRecordFileByUniqueIdQuery),
            file_converter=file_converter,
            logger=logger,
            enable_conversion=config.enable_conversion,

        )

        app.add_api_route(
            path="/records/{unique_id}",
            endpoint=call_records_view.handle,
            methods=["GET"],
            tags=["Records"]
        )

    async def unload(self) -> None:
        self.__dispatcher.delete_function(IGenerateLinkFunction)

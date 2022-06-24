from typing import Any
from typing import Mapping

from fastapi import FastAPI
from glassio.dispatcher import IDispatcher
from glassio.logger import ILogger

from amocrm_asterisk_ng.domain import IGetRecordFileUniqueIdQuery

from .CallRecordsConfig import CallRecordsConfig
from .file_converters import PydubFileConverter
from .views import CallRecordsView


__all__ = [
    "call_records_startup",
]


def call_records_startup(
    settings: Mapping[str, Any],
    app: FastAPI,
    dispatcher: IDispatcher,
    logger: ILogger,
) -> None:

    config = CallRecordsConfig(**settings)

    get_cdr_by_unique_id_query = dispatcher.get_function(IGetRecordFileUniqueIdQuery)

    call_records_view = CallRecordsView(
        config=config,
        get_cdr_by_unique_id_query=get_cdr_by_unique_id_query,
        file_converter=PydubFileConverter(config=config),
        logger=logger,
    )

    app.add_api_route(
        path="/amocrm/records/{unique_id}",
        endpoint=call_records_view.handle,
        methods=["GET"],
    )

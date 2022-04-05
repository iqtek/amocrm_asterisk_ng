from typing import Mapping
from typing import Any

from fastapi import FastAPI
from asterisk_amocrm.infrastructure import IDispatcher, ILogger
from .views import CallRecordsView
from asterisk_amocrm.domains import IGetCdrByUniqueIdQuery
from .CallRecordsConfig import CallRecordsConfig
from .file_converters import PydubFileConverter
__all__ = [
    "call_records_startup",
]


def call_records_startup(
    settings: Mapping[str, Any],
    endpoint_format_string: str,
    app: FastAPI,
    dispatcher: IDispatcher,
    logger: ILogger,
) -> None:

    config = CallRecordsConfig(**settings)

    get_cdr_by_unique_id_query = dispatcher.get_function(IGetCdrByUniqueIdQuery)

    call_records_view = CallRecordsView(
        get_cdr_by_unique_id_query=get_cdr_by_unique_id_query,
        file_converter=PydubFileConverter(config=config),
        logger=logger,
    )

    app.add_api_route(
        path=endpoint_format_string,
        endpoint=call_records_view.handle,
        methods=["GET"],
    )

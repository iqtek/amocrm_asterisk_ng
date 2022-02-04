from fastapi import FastAPI
from asterisk_amocrm.infrastructure import IDispatcher, ILogger
from .CallRecordsView import CallRecordsView


__all__ = [
    "call_records_startup",
]


def call_records_startup(
    app: FastAPI,
    dispatcher: IDispatcher,
    logger: ILogger,
) -> None:

    call_records_view = CallRecordsView(
        dispatcher=dispatcher,
        logger=logger,
    )
    app.add_api_route(
        path="/amocrm/cdr/{unique_id}.mp3",
        endpoint=call_records_view.handle,
        methods=["GET"],
    )

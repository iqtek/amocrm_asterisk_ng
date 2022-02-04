import logging
from logging import (
    config,
    LoggerAdapter,
)
from typing import (
    Optional,
    Dict,
    Any,
)
from ..core import ILogger
from asterisk_amocrm.infrastructure.context_vars import trace_id

__all__ = [
    "logger_startup",
]


class TraceAdapter(LoggerAdapter):

    def process(self, msg, kwargs):
        context_var = self.extra.get("context_vars")
        if context_var:
            try:
                value = context_var.get()
            except LookupError:
                return msg, kwargs
            msg += f" trace-id: {value}"
        return msg, kwargs


def logger_startup(
    name: Optional[str] = "root",
    settings: Optional[Dict[str, Any]] = None,
) -> ILogger:
    if settings:
        config.dictConfig(settings)
    logger = logging.getLogger(name)
    adapter = TraceAdapter(logger, extra={"context_vars": trace_id})
    return adapter


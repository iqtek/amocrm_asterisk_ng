from logging import Logger

from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from amocrm_asterisk_ng.infrastructure import ioc

from .TraceIdFilter import TraceIdFilter
from .TracingMiddleware import TracingMiddleware


__all__ = [
    "tracing_startup",
]


def tracing_startup() -> None:
    app = ioc.get_instance(FastAPI)
    app.add_middleware(BaseHTTPMiddleware, dispatch=TracingMiddleware())
    logger = ioc.get_instance(Logger)
    logger.addFilter(TraceIdFilter())

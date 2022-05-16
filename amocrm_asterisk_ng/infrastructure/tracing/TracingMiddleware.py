from fastapi import Request
from glassio.context import set_context

from .generate_trace_id import generate_trace_id


__all__ = [
    "TracingMiddleware",
]


class TracingMiddleware:

    __slots__ = ()

    async def __call__(self, request: Request, call_next):
        trace_id = generate_trace_id()
        set_context({"trace_id": trace_id})
        response = await call_next(request)
        return response

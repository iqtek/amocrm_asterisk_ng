from contextvars import ContextVar


__all__ = [
    "trace_id",
]


trace_id: ContextVar[str] = ContextVar('trace_id')

from contextvars import ContextVar

from typing import Optional


__all__ = [
    "set_trace_id",
    "get_trace_id",
]


CONTEXT_VAR: ContextVar[str] = ContextVar("trace_id")

def set_trace_id(trace_id: str) -> None:
    CONTEXT_VAR.set(trace_id)

def get_trace_id() -> Optional[str]:
    try:
        return CONTEXT_VAR.get()
    except LookupError:
        return None

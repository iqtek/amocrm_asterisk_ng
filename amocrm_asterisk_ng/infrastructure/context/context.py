from contextvars import ContextVar

from typing import Any
from typing import Hashable
from typing import Mapping
from typing import MutableMapping

from uuid import uuid4


__all__ = [
    "get_context",
    "set_context",
    "update_context",
    "clear_context",
]


context_var_name = f"context_{str(uuid4())}"


context_var: ContextVar[MutableMapping[Hashable, Any]] = ContextVar(context_var_name)


def get_context() -> MutableMapping[Hashable, Any]:
    try:
        return context_var.get()
    except LookupError:
        context_var.set({})
        return context_var.get()


def set_context(context: Mapping[Hashable, Any]) -> None:
    current_context = get_context()
    current_context.clear()
    current_context.update(context)


def update_context(context: Mapping[Hashable, Any]) -> None:
    current_context = get_context()
    current_context.update(context)


def clear_context() -> None:
    current_context = get_context()
    current_context.clear()

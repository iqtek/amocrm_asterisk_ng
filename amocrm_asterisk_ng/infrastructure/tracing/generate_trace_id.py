from time import time


__all__ = [
    "generate_trace_id",
]


def generate_trace_id() -> str:
    return str(time())

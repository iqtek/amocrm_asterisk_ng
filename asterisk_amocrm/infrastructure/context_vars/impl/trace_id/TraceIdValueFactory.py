import time
from ...core import IValueFactory


__all__ = [
    "TraceIdValueFactory",
]


class TraceIdValueFactory(IValueFactory):

    def __call__(self) -> str:
        return str(time.time())

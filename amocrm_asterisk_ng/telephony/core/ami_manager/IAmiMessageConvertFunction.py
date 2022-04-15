from panoramisk.message import Message

from .packets import Event


__all__ = [
    "IAmiMessageConvertFunction",
]


class IAmiMessageConvertFunction:

    __slots__ = ()

    def __call__(self, message: Message) -> Event:
        raise NotImplementedError()

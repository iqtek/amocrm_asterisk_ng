from panoramisk.message import Message

from .....core import (
    Event,
    IAmiMessageConvertFunction,
)


__all__ = [
    "AmiMessageConvertFunctionImpl",
]


class AmiMessageConvertFunctionImpl(IAmiMessageConvertFunction):

    def __call__(self, message: Message) -> Event:
        params = dict(message.items())
        name = params.pop("Event")
        id = params.pop("ActionID", None)
        parameters = {key: value for key, value in params.items()
                      if value != "<unknown>" and value != ""}
        return Event(name, parameters, id)

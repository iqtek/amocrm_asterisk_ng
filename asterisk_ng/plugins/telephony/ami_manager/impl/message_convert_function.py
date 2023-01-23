from panoramisk.message import Message

from ..core import Event


__all__ = ["message_convert_function"]


def message_convert_function(message: Message) -> Event:
    params = dict(message.items())
    name = params.pop("Event")
    id = params.pop("ActionID", None)
    parameters = {key: value for key, value in params.items()
                  if value != "<unknown>" and value != ""}
    return Event(name, parameters, id)

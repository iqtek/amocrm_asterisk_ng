from typing import Any
from typing import Mapping
from typing import MutableMapping
from typing import Optional
from typing import Tuple
from typing import Type

from glassio.event_bus import EventDeserializationException
from glassio.event_bus import EventSerializationException
from glassio.event_bus import IEventSerializer
import ujson

from .BaseEvent import BaseEvent


__all__ = [
    "EventSerializer",
]


class EventSerializer(IEventSerializer[BaseEvent]):

    __ENCODING = "utf-8"

    __slots__ = (
        "__event_types",
    )

    def __init__(self) -> None:
        self.__event_types: MutableMapping[str, Type[BaseEvent]] = {}

    def serialize(self, event: BaseEvent) -> Tuple[bytes, Optional[str]]:
        try:
            payload = ujson.dumps(event.dict()).encode(self.__ENCODING)
        except TypeError:
            raise EventSerializationException(
                f"Non-serializable event: `{event}`."
            )
        event_name = event.__class__.__name__
        self.__event_types[event_name] = type(event)
        return payload, event_name

    def deserialize(self, serialized_event: bytes, event_type: Optional[str]) -> BaseEvent:
        if event_type is None:
            raise EventDeserializationException(
                f"Serialized_event: `{serialized_event}` "
                f"event_type: `{event_type}`."
            )
        json_str = serialized_event.decode(self.__ENCODING)
        event_data: Mapping[str, Any] = ujson.loads(json_str)
        try:
            type_of_event = self.__event_types[event_type]
        except KeyError as exc:
            raise EventDeserializationException(f"Unknown event type: `{event_type}`.") from exc
        event = type_of_event(**event_data)
        return event

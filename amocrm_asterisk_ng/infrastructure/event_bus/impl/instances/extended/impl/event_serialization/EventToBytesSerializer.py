import ujson

from ...core import IRegisteringFactory
from ...core import ISerializer
from .....event import to_mapping
from ......core import IEvent


__all__ = [
    "EventToBytesSerializer",
]


class EventToBytesSerializer(ISerializer[IEvent, bytes]):

    __BYTES_ENCODING = "utf-8"

    __slots__ = (
        "__event_factory",
    )

    def __init__(
        self,
        event_factory: IRegisteringFactory[IEvent],
    ) -> None:
        self.__event_factory = event_factory

    def serialize(self, obj: IEvent) -> bytes:
        payload = to_mapping(obj)
        event_name = obj.__class__.__name__
        mapping = {
            "name": event_name,
            "message": payload,
        }
        str_result: str = ujson.dumps(mapping)
        return str_result.encode(self.__BYTES_ENCODING)

    def deserialize(self, serialized_data: bytes) -> IEvent:
        str_data = serialized_data.decode(encoding=self.__BYTES_ENCODING)
        data = ujson.loads(str_data)

        event_name = data["name"]
        event_data = data["message"]

        event = self.__event_factory.get_instance(
            type_name=event_name,
            **event_data
        )
        return event

from typing import Dict
from datetime import datetime

import pytest

from amocrm_asterisk_ng.infrastructure.event_bus import IEvent
from amocrm_asterisk_ng.infrastructure.event_bus import BaseEvent
from amocrm_asterisk_ng.infrastructure.event_bus.impl.instances.extended.core import ISerializer
from amocrm_asterisk_ng.infrastructure.event_bus.impl.instances.extended.impl.event_serialization import EventToBytesSerializer
from amocrm_asterisk_ng.infrastructure.event_bus.impl.instances.extended.core import IRegisteringFactory
from amocrm_asterisk_ng.infrastructure.event_bus.impl.instances.extended.impl.event_serialization.RegisteringFactory import RegisteringFactory


def test_serializer() -> None:

    class MyEvent(BaseEvent):
        value: int
        string: str
        dictionary: Dict

    event_factory: IRegisteringFactory[IEvent] = RegisteringFactory()
    serializer: ISerializer[IEvent, bytes] = EventToBytesSerializer(
        event_factory=event_factory
    )
    event = MyEvent(
        value=10,
        string="foo",
        dictionary={
            "data": "bar",
        }
    )
    event_factory.register_type("MyEvent", MyEvent)
    serialized_event = serializer.serialize(event)
    deserialized_event = serializer.deserialize(serialized_event)
    assert event == deserialized_event


def test_serialize_non_serialized_event() -> None:

    class NonSerializedEvent(BaseEvent):
        date: datetime

    event_factory: IRegisteringFactory[IEvent] = RegisteringFactory()
    serializer: ISerializer[IEvent, bytes] = EventToBytesSerializer(
        event_factory=event_factory
    )
    event = NonSerializedEvent(
        date=datetime(2022, 1, 1)
    )
    event_factory.register_type("NonSerializedEvent", NonSerializedEvent)
    with pytest.raises(Exception):
        serializer.serialize(event)

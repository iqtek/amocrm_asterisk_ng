import asyncio

import pytest
import random

from amocrm_asterisk_ng.infrastructure import Message
from amocrm_asterisk_ng.infrastructure.message_bus import Properties
from amocrm_asterisk_ng.infrastructure.message_bus import IConsumer

from .consumers import SimpleConsumer
from .consumers import ToggleConsumer


@pytest.mark.asyncio
async def test_consumer_call(initialized_message_bus) -> None:
    """
    The consumer must receive the message and be called once.
    """

    published_message = b"some message"

    consumer = SimpleConsumer()

    await initialized_message_bus.add_consumer(consumer)
    await initialized_message_bus.publish(published_message)
    await asyncio.sleep(0.001)

    assert consumer.call_counter == 1
    assert consumer.consumed_message == published_message


@pytest.mark.asyncio
async def test_of_calling_multiple_consumers(initialized_message_bus) -> None:
    """
    The number of messages published must be equal to the
    number of messages consumed.
    Each consumer must be called at least once.
    """

    number_of_publications = 20
    published_message = b"some message"

    consumers = [SimpleConsumer() for _ in range(10)]

    for consumer in consumers:
        await initialized_message_bus.add_consumer(consumer)

    for _ in range(number_of_publications):
        await initialized_message_bus.publish(published_message)

    await asyncio.sleep(0.001)

    total_calls = sum([consumers.call_counter for consumers in consumers])

    assert total_calls == number_of_publications

    for consumer in consumers:
        assert consumer.call_counter < 20
        assert consumer.call_counter > 0


@pytest.mark.asyncio
async def test_publish_with_empty_properties(initialized_message_bus) -> None:

    published_message = b"some line"

    consumer = SimpleConsumer()

    await initialized_message_bus.add_consumer(consumer)
    await initialized_message_bus.publish(published_message)
    await asyncio.sleep(0.001)

    assert isinstance(consumer.consumed_properties, Properties)


@pytest.mark.asyncio
async def test_publish_with_properties(initialized_message_bus) -> None:

    published_message = b"some line"
    message_properties = Properties(
        headers={
            "foo": b"bar",
            "baz": 1,
            "empty_byte_str": b"",
        },
    )

    consumer = SimpleConsumer()

    await initialized_message_bus.add_consumer(consumer)
    await initialized_message_bus.publish(published_message, properties=message_properties)
    await asyncio.sleep(0.001)
    assert consumer.consumed_properties == message_properties


@pytest.mark.asyncio
async def test_message_rejecting(initialized_message_bus) -> None:

    published_message = b"some line"

    consumer = ToggleConsumer()

    await initialized_message_bus.add_consumer(consumer)
    await initialized_message_bus.publish(published_message)
    await asyncio.sleep(0.01)

    assert consumer.call_counter == 2


@pytest.mark.asyncio
async def test_message_expiration(initialized_message_bus) -> None:

    published_message = b"expiration message"

    properties = Properties(
        expiration=0.01,
    )
    consumer = SimpleConsumer()

    await initialized_message_bus.publish(
        published_message,
        properties=properties,
    )
    await asyncio.sleep(0.1)
    await initialized_message_bus.add_consumer(consumer)

    await asyncio.sleep(0.001)

    assert consumer.call_counter == 0


@pytest.mark.asyncio
async def test_consume_of_unexpired_message(initialized_message_bus) -> None:

    published_message = b"some line"
    properties = Properties(
        expiration=1,
    )
    consumer = SimpleConsumer()

    await initialized_message_bus.publish(
        published_message,
        properties=properties,
    )
    await initialized_message_bus.add_consumer(consumer)
    await asyncio.sleep(0.01)

    assert consumer.call_counter == 1


@pytest.mark.asyncio
async def test_message_priority(initialized_message_bus) -> None:

    numbers = list(range(10))
    random.shuffle(numbers)

    for number in numbers:
        priority = number

        await initialized_message_bus.publish(
            b"anything",
            properties=Properties(
                priority=priority,
            ),
        )

    class Consumer(IConsumer):

        __slots__ = (
            "__previous_priority"
        )

        def __init__(self) -> None:
            self.__previous_priority: int = 10

        async def __call__(self, message: Message, properties: Properties) -> None:
            print(self.__previous_priority)
            test_result = properties.priority <= self.__previous_priority
            self.__previous_priority = properties.priority

    consumer = Consumer()
    await initialized_message_bus.add_consumer(consumer)
    await asyncio.sleep(0.1)

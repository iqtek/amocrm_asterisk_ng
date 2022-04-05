import asyncio

import pytest

from asterisk_amocrm.infrastructure.event_bus import (
    HandlerAlreadyAttachedException,
    HandlerNotAttachedFoundException,
    IEvent,
    IEventBus,
    BaseEvent,
    IEventHandler,
)


class MyEvent(BaseEvent):
    version: int
    field: str


@pytest.mark.asyncio
async def test_attach_invalid_handler(event_bus):

    class InvalidHandler(IEventHandler):

        async def __call__(self, foo: str) -> None:
            pass

    await event_bus.initialize()

    with pytest.raises(AttributeError):
        await event_bus.attach_event_handler(InvalidHandler())

    await event_bus.deinitialize()


@pytest.mark.asyncio
async def test_handler_reconnect(event_bus):

    class Handler(IEventHandler):

        async def __call__(self, event: MyEvent) -> None:
            pass

    await event_bus.initialize()
    await event_bus.attach_event_handler(Handler())
    with pytest.raises(HandlerAlreadyAttachedException):
        await event_bus.attach_event_handler(Handler())
    await event_bus.deinitialize()


@pytest.mark.asyncio
async def test_detach_non_existent_handler(event_bus):

    class Handler(IEventHandler):

        async def __call__(self, event: MyEvent) -> None:
            pass

    await event_bus.initialize()
    with pytest.raises(HandlerNotAttachedFoundException):
        await event_bus.detach_event_handler(Handler)
    await event_bus.deinitialize()


@pytest.mark.asyncio
async def test_trigger_handler(event_bus):

    handler_was_called: bool = False

    class TestEventHandler(IEventHandler):

        async def __call__(self, event: MyEvent) -> None:
            nonlocal handler_was_called
            handler_was_called = True
            # assert isinstance(event, MyEvent)

    await event_bus.initialize()
    await event_bus.attach_event_handler(TestEventHandler())
    await event_bus.publish(
        MyEvent(
            version=1,
            field="bar",
        )
    )
    await asyncio.sleep(0.1)
    await event_bus.deinitialize()
    assert handler_was_called


@pytest.mark.asyncio
async def test_trigger_many_handler(event_bus):

    call_counter: int = 0

    class TestEventFirstHandler(IEventHandler):

        async def __call__(self, event: MyEvent) -> None:
            nonlocal call_counter
            call_counter += 1
            # assert isinstance(event, MyEvent)

    class TestEventSecondHandler(IEventHandler):

        async def __call__(self, event: MyEvent) -> None:
            nonlocal call_counter
            call_counter += 1
            # assert isinstance(event, MyEvent)

    await event_bus.initialize()
    await event_bus.attach_event_handler(TestEventFirstHandler())
    await event_bus.attach_event_handler(TestEventSecondHandler())
    await event_bus.publish(
        MyEvent(
            version=1,
            field="foo"
        )
    )
    await asyncio.sleep(0.002)
    await event_bus.deinitialize()

    assert call_counter == 2

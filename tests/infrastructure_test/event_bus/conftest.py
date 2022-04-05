import asyncio

import pytest

from asterisk_amocrm.infrastructure.event_bus import get_event_bus
from asterisk_amocrm.infrastructure.event_bus import IEventBus


extended_event_bus_settings = {
    "type": "extended",
    "settings": {},
}


memory_event_bus_settings = {
    "type": "memory",
    "settings": {},
}


@pytest.fixture(params=[
    extended_event_bus_settings,
    memory_event_bus_settings
])
async def event_bus(
    request,
    initialized_message_bus,
    logger,
    set_context_vars_function,
    make_context_vars_snapshot,
) -> IEventBus:
    event_loop = asyncio.get_event_loop()
    event_bus = get_event_bus(
        request.param,
        message_bus=initialized_message_bus,
        event_loop=event_loop,
        logger=logger,
        set_context_vars_function=set_context_vars_function,
        make_context_vars_snapshot=make_context_vars_snapshot,
    )
    return event_bus

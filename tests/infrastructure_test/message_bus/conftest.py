import asyncio

import pytest

from amocrm_asterisk_ng.infrastructure.message_bus import get_message_bus
from amocrm_asterisk_ng.infrastructure.message_bus import InitializableMessageBus


memory_message_bus_settings = {"type": "memory"}
rabbitmq_message_bus_settings = {"type": "rabbitmq", "settings": {"port": 5672}}


@pytest.fixture(params=[
    memory_message_bus_settings,
    rabbitmq_message_bus_settings,
])
def message_bus(
    request,
    get_current_version_function,
    logger,
) -> InitializableMessageBus:

    message_bus = get_message_bus(
        settings=request.param,
        get_app_version_function=get_current_version_function,
        event_loop=asyncio.get_event_loop(),
        logger=logger,
    )
    return message_bus


@pytest.fixture()
async def initialized_message_bus(message_bus):
    await message_bus.initialize()
    yield message_bus
    await message_bus.deinitialize()

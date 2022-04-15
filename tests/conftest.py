import asyncio
from typing import Optional

import pytest

from amocrm_asterisk_ng.infrastructure import ContextSnapshot
from amocrm_asterisk_ng.infrastructure.message_bus import get_message_bus
from amocrm_asterisk_ng.infrastructure.message_bus import InitializableMessageBus

from amocrm_asterisk_ng.infrastructure.get_version import (
    IGetCurrentAppVersionFunction,
    GetCurrentAppVersionFunction,
    Version,
)
from amocrm_asterisk_ng.infrastructure.context_vars import ISetContextVarsFunction
from amocrm_asterisk_ng.infrastructure.context_vars import IMakeContextSnapshotFunction
from amocrm_asterisk_ng.infrastructure.context_vars import ContextSnapshot

from amocrm_asterisk_ng.infrastructure.logger import ILogger, get_logger


@pytest.fixture()
def set_context_vars_function() -> ISetContextVarsFunction:

    class SetContextVarsFunction(ISetContextVarsFunction):

        def __call__(self, snapshot: Optional[ContextSnapshot] = None) -> None:
            pass

    return SetContextVarsFunction()


@pytest.fixture()
def make_context_vars_snapshot() -> IMakeContextSnapshotFunction:

    class MakeContextSnapshotFunction(IMakeContextSnapshotFunction):
        def __call__(self) -> ContextSnapshot:
            context = ContextSnapshot()
            return context

    return MakeContextSnapshotFunction()


@pytest.fixture()
def get_current_version_function() -> IGetCurrentAppVersionFunction:
    version = Version(1, 0, 0)
    return GetCurrentAppVersionFunction(version)


@pytest.fixture()
def logger() -> ILogger:
    return get_logger({})


@pytest.fixture()
async def initialized_message_bus(
    get_current_version_function,
    logger,
) -> InitializableMessageBus:

    memory_message_bus_settings = {"type": "memory"}

    message_bus = get_message_bus(
        settings=memory_message_bus_settings,
        get_app_version_function=get_current_version_function,
        event_loop=asyncio.get_event_loop(),
        logger=logger,
    )
    await message_bus.initialize()
    yield message_bus
    await message_bus.deinitialize()

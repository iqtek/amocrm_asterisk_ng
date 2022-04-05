import pytest

from asterisk_amocrm.infrastructure.get_version import (
    IGetCurrentAppVersionFunction,
    GetCurrentAppVersionFunction,
    Version,
)
from asterisk_amocrm.infrastructure import ILogger, get_logger


@pytest.fixture()
def get_current_version_function() -> IGetCurrentAppVersionFunction:
    version = Version(1, 0, 0)
    return GetCurrentAppVersionFunction(version)


@pytest.fixture()
def logger() -> ILogger:
    return get_logger({})

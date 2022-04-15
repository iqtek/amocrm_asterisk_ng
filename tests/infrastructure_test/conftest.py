import pytest

from amocrm_asterisk_ng.infrastructure.get_version import (
    IGetCurrentAppVersionFunction,
    GetCurrentAppVersionFunction,
    Version,
)
from amocrm_asterisk_ng.infrastructure import ILogger, get_logger


@pytest.fixture()
def get_current_version_function() -> IGetCurrentAppVersionFunction:
    version = Version(1, 0, 0)
    return GetCurrentAppVersionFunction(version)


@pytest.fixture()
def logger() -> ILogger:
    return get_logger({})

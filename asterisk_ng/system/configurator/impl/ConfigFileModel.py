from pydantic import BaseModel

from asterisk_ng.system.configurator.core.models import DynamicConfiguration
from asterisk_ng.system.configurator.core.models import StaticConfiguration


__all__ = ["ConfigFileModel"]


class ConfigFileModel(BaseModel):
    static: StaticConfiguration
    dynamic: DynamicConfiguration

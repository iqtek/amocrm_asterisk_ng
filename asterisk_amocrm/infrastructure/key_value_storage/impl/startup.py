from typing import Any
from typing import Mapping

from asterisk_amocrm.infrastructure import ioc
from asterisk_amocrm.infrastructure import SelectorImpl
from asterisk_amocrm.infrastructure import ISelector
from asterisk_amocrm.infrastructure import ILogger
from asterisk_amocrm.infrastructure import SelectedComponentConfig

from ..core import IKeyValueStorageFactory
from .instances import RedisKeyValueStorageFactory


__all__ = [
    "storage_startup",
]


def storage_startup(
    settings: Mapping[str, Any],
) -> None:
    startup_config = SelectedComponentConfig(**settings)

    logger = ioc.get_instance(ILogger)

    selector: ISelector = SelectorImpl()
    selector.add_item(
        RedisKeyValueStorageFactory(
            settings=startup_config.settings,
            logger=logger,
        )
    )
    factory = selector.get_item(
        unique_tag=startup_config.type,
    )

    ioc.set_instance(
        key=IKeyValueStorageFactory,
        instance=factory,
    )

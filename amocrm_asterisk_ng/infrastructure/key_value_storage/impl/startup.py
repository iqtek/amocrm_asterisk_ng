from typing import Any
from typing import Mapping

from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure import SelectorImpl
from amocrm_asterisk_ng.infrastructure import ISelector
from amocrm_asterisk_ng.infrastructure import ILogger
from amocrm_asterisk_ng.infrastructure import SelectedComponentConfig

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

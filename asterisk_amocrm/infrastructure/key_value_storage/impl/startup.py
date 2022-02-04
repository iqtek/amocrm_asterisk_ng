from typing import (
    Optional,
    Mapping,
    Any,
)

from asterisk_amocrm.infrastructure.logger import ILogger
from pydantic import ValidationError
from .FactoryStoreImpl import FactoryStoreImpl
from .KeyValueStorageConfigModel import KeyValueStorageConfigModel
from .KeyValueStorageSettingsModel import KeyValueStorageSettingsModel
from .instances import RedisKeyValueStorageFactory
from ..core import IKeyValueStorageFactory


__all__ = [
    "storage_startup",
]


def storage_startup(
    logger: ILogger,
    settings: Optional[Mapping[str, Any]] = None,
    config: Optional[KeyValueStorageConfigModel] = None,
) -> IKeyValueStorageFactory:
    if not config:
        try:
            config = KeyValueStorageConfigModel(**settings)
        except (ValidationError, TypeError):
            pass
    settings = settings or {}
    settings = KeyValueStorageSettingsModel(**settings)

    if config:
        storage_config = config.storage_config
        selected_type = config.type
    else:
        selected_type = settings.type
        storage_config = None

    factory_store = FactoryStoreImpl()

    factory_store.register_factory(
        RedisKeyValueStorageFactory(
            settings=settings.storage_settings,
            config=storage_config,
            logger=logger,
        )
    )
    storage_factory = factory_store.get_instance(
        type=selected_type,
    )

    return storage_factory

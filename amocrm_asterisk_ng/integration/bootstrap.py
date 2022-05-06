from amocrm_asterisk_ng.crm import crm_startup
from amocrm_asterisk_ng.infrastructure import dispatcher_startup
from amocrm_asterisk_ng.infrastructure import event_bus_startup
from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure import logger_startup
from amocrm_asterisk_ng.infrastructure import storage_startup
from amocrm_asterisk_ng.scenario import scenario_startup
from amocrm_asterisk_ng.telephony import telephony_startup

from .IntegrationConfig import IntegrationConfig


__all__ = [
    "bootstrap",
]


def bootstrap() -> None:
    config = ioc.get_instance(IntegrationConfig)

    logger_startup(
        settings=config.infrastructure.logger,
    )

    storage_startup(
        settings=config.infrastructure.storage,
    )

    dispatcher_startup()

    event_bus_startup(settings={"type": "memory"})

    scenario_startup(
        scenario_name=config.scenario,
        scenario_configs_dir=config.scenario_configs_dir
    )

    crm_startup(settings=config.crm)

    telephony_startup(settings=config.telephony)

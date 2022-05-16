from glassio.dispatcher import IDispatcher
from glassio.dispatcher import LocalDispatcher
from glassio.logger import ILogger

from amocrm_asterisk_ng.crm import crm_startup
from amocrm_asterisk_ng.infrastructure import glassio_logger_startup
from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure import logger_startup
from amocrm_asterisk_ng.infrastructure import storage_startup
from amocrm_asterisk_ng.infrastructure import tracing_startup
from amocrm_asterisk_ng.infrastructure.event_bus.startup import event_bus_startup
from amocrm_asterisk_ng.scenario import scenario_startup
from amocrm_asterisk_ng.telephony import telephony_startup

from .IntegrationConfig import IntegrationConfig


__all__ = [
    "bootstrap",
]


def bootstrap() -> None:
    config = ioc.get_instance(IntegrationConfig)

    logger_startup(config.infrastructure.logger)
    tracing_startup()
    glassio_logger_startup()
    storage_startup(settings=config.infrastructure.storage)

    logger = ioc.get_instance(ILogger)
    dispatcher = LocalDispatcher(logger)
    ioc.set_instance(IDispatcher, dispatcher)

    event_bus_startup()

    scenario_startup(
        scenario_name=config.scenario,
        scenario_configs_dir=config.scenario_configs_dir
    )

    crm_startup(settings=config.crm)
    telephony_startup(settings=config.telephony)

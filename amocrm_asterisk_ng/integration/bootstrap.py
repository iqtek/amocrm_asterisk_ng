from logging import config as logging_config

from glassio.dispatcher import IDispatcher
from glassio.dispatcher import LocalDispatcher
from glassio.logger import ILogger
from glassio.logger import InitializableLogger
from glassio.logger import StandardLoggerFactory

from amocrm_asterisk_ng.crm import crm_startup
from amocrm_asterisk_ng.infrastructure import ioc
from amocrm_asterisk_ng.infrastructure import storage_startup
from amocrm_asterisk_ng.infrastructure.event_bus.startup import event_bus_startup
from amocrm_asterisk_ng.scenario import scenario_startup
from amocrm_asterisk_ng.telephony import telephony_startup

from .IntegrationConfig import IntegrationConfig


__all__ = [
    "bootstrap",
]


def bootstrap() -> None:
    config = ioc.get_instance(IntegrationConfig)

    if len(config.infrastructure.logger.keys()) != 0:
        logging_config.dictConfig(config.infrastructure.logger)

    logger_factory = StandardLoggerFactory()
    logger = logger_factory("root")
    ioc.set_instance(InitializableLogger, logger)
    ioc.set_instance(ILogger, logger)

    storage_startup(settings=config.infrastructure.storage)

    dispatcher = LocalDispatcher(logger)
    ioc.set_instance(IDispatcher, dispatcher)

    event_bus_startup()

    scenario_startup(
        scenario_name=config.scenario,
        scenario_configs_dir=config.scenario_configs_dir
    )

    crm_startup(settings=config.crm)
    telephony_startup(settings=config.telephony)

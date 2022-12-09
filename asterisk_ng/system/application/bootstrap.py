from logging import config
from logging import getLogger

from asterisk_ng.plugins.crm_system.amocrm.kernel.amo_client import AmoClientPluginFactory
from asterisk_ng.plugins.crm_system.amocrm.kernel.functions import AmocrmFunctionsPluginFactory
from asterisk_ng.plugins.crm_system.amocrm.kernel.records import AmocrmRecordsProviderPluginFactory
from asterisk_ng.plugins.crm_system.amocrm.widgets.asterisk import AsteriskWidgetPluginFactory
from asterisk_ng.plugins.crm_system.amocrm.widgets.asterisk_ng import AsteriskNgWidgetPluginFactory

from asterisk_ng.plugins.domain import StandardDomainPluginFactory

from asterisk_ng.plugins.system.converter import FileConverterPluginFactory
from asterisk_ng.plugins.system.fastapi import FastapiPluginFactory
from asterisk_ng.plugins.system.storage import StoragePluginFactory

from asterisk_ng.plugins.telephony.ami_manager import AmiManagerPluginFactory
from asterisk_ng.plugins.telephony.asterisk_16.functions import Asterisk16FunctionPluginFactory
from asterisk_ng.plugins.telephony.asterisk_16.records_provider import RecordsProviderPluginFactory
from asterisk_ng.plugins.telephony.asterisk_16.reflector import ReflectorPluginFactory
from asterisk_ng.plugins.telephony.redirecting import RedirectingPluginFactory


from asterisk_ng.system.configurator import StaticConfiguration
from asterisk_ng.system.container import container, Key, SingletonResolver
from asterisk_ng.system.dispatcher import IDispatcher, LocalDispatcher
from asterisk_ng.system.event_bus import EventBusImpl, IEventBus
from asterisk_ng.system.logger import ILogger, StandardLogger
from asterisk_ng.system.plugin_store import PluginStore


__all__ = ["bootstrap"]


def bootstrap(configuration: StaticConfiguration) -> None:

    # Logger.

    logger_settings = configuration.logger

    if len(logger_settings.keys()) != 0:
        config.dictConfig(dict(logger_settings))

    logger = StandardLogger(getLogger("root"))
    container.set_resolver(Key(ILogger), SingletonResolver(logger))

    # Dispatcher.

    dispatcher = LocalDispatcher(logger=logger)
    container.set_resolver(Key(IDispatcher), SingletonResolver(dispatcher))

    # EventBus.

    event_bus = EventBusImpl(logger=logger)
    container.set_resolver(Key(IEventBus), SingletonResolver(event_bus))

    # PluginStore.

    plugin_store_logger = logger

    plugin_store = PluginStore(
        {
            "amocrm.amoclient": AmoClientPluginFactory(),
            "amocrm.functions": AmocrmFunctionsPluginFactory(),
            "amocrm.widget.asterisk": AsteriskWidgetPluginFactory(),
            "amocrm.records.provider": AmocrmRecordsProviderPluginFactory(),
            "amocrm.widget.asterisk_ng": AsteriskNgWidgetPluginFactory(),

            "standard.domain": StandardDomainPluginFactory(),

            "telephony.redirecting": RedirectingPluginFactory(),
            "telephony.ami_manager": AmiManagerPluginFactory(),
            "telephony.asterisk16.reflector": ReflectorPluginFactory(),
            "telephony.asterisk16.functions": Asterisk16FunctionPluginFactory(),
            "telephony.records_provider": RecordsProviderPluginFactory(),

            "system.converter": FileConverterPluginFactory(),
            "system.storage": StoragePluginFactory(),
            "system.fastapi": FastapiPluginFactory(),

        },
        logger=plugin_store_logger,
    )
    container.set_resolver(Key(PluginStore), SingletonResolver(plugin_store))

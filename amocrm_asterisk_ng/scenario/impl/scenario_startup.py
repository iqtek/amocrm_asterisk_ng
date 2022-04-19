from amocrm_asterisk_ng.infrastructure import IDispatcher
from amocrm_asterisk_ng.infrastructure import InitializableEventBus
from amocrm_asterisk_ng.infrastructure import ioc

from .get_scenario import get_scenario
from ..core import IScenario


__all__ = [
    "scenario_startup",
]


def scenario_startup(scenario_name: str) -> None:

    event_bus = ioc.get_instance(InitializableEventBus)
    dispatcher = ioc.get_instance(IDispatcher)

    scenario = get_scenario(
        scenario_name=scenario_name,
        event_bus=event_bus,
        dispatcher=dispatcher,
    )

    ioc.set_instance(IScenario, scenario)

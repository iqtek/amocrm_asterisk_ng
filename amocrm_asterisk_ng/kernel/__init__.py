from typing import Type


from ....core import IScenarioFactory
from .ClassicScenarioFactory import ClassicScenarioFactory


__all__ = ["SCENARIO_FACTORY"]


SCENARIO_FACTORY: Type[IScenarioFactory] = ClassicScenarioFactory

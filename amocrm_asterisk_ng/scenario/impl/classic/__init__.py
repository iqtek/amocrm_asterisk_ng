from typing import Type

from glassio.mixins import IFactory

from ...core import IScenario
from .ClassicScenarioFactory import ClassicScenarioFactory


__all__ = ["SCENARIO_FACTORY", "ClassicScenarioFactory"]


SCENARIO_FACTORY: Type[IFactory[IScenario]] = ClassicScenarioFactory

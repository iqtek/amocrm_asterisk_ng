from typing import Type

from glassio.mixins import IFactory

from .ClassicScenarioFactory import ClassicScenarioFactory
from ...core import IScenario


__all__ = ["SCENARIO_FACTORY"]


SCENARIO_FACTORY: Type[IFactory[IScenario]] = ClassicScenarioFactory

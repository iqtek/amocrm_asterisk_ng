from typing import Optional

from ....core import InitializableComponent
from ...abstract import AbstractInitializableComponent

from ..sequential import SequentialInitializer

from .Graph import Graph
from .exceptions import CycleFoundException
from .utils import get_cycle
from .utils import topological_sort


__all__ = [
    "GraphInitializer",
]


class GraphInitializer(AbstractInitializableComponent):

    __slots__ = (
        "__sequential_initializer",
    )

    def __init__(self, graph: Graph[InitializableComponent], name: Optional[str] = None) -> None:
        super().__init__(name=name)
        try:
            sequence = topological_sort(graph)
        except CycleFoundException as exc:
            cycle = get_cycle(graph)
            raise CycleFoundException(cycle=cycle) from exc
        self.__sequential_initializer = SequentialInitializer(sequence, name=name)

    async def _initialize(self) -> None:
        await self.__sequential_initializer.initialize()

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:
        await self.__sequential_initializer.deinitialize(exception=exception)

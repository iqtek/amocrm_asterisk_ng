from typing import Optional
from typing import Sequence

from ....core import InitializableComponent
from ...abstract import AbstractInitializableComponent
from ...standard import InitializedState


__all__ = [
    "SequentialInitializer",
]


class SequentialInitializer(AbstractInitializableComponent):

    __slots__ = (
        "__component_sequence"
    )

    def __init__(
        self,
        components: Sequence[InitializableComponent],
        name: Optional[str] = None
    ) -> None:
        super().__init__(name=name)
        self.__component_sequence = tuple(components)

    async def _initialize(self) -> None:
        try:
            for component in self.__component_sequence:
                await component.initialize()
        except Exception as exc:
            await self._deinitialize(exc)
            raise exc

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:

        for component in reversed(self.__component_sequence):
            if issubclass(type(component.state), InitializedState):
                await component.deinitialize(exception)

from asyncio import ALL_COMPLETED
from asyncio import create_task
from asyncio import wait

from typing import Collection
from typing import Optional

from ....core import InitializableComponent
from ...abstract import AbstractInitializableComponent
from ...standard import InitializedState


__all__ = [
    "ParallelInitializer",
]


class ParallelInitializer(AbstractInitializableComponent):

    __slots__ = (
        "__components",
    )

    def __init__(
        self,
        components: Collection[InitializableComponent],
        name: Optional[str] = None
    ) -> None:
        super().__init__(name=name)
        self.__components = frozenset(components)

    async def _initialize(self) -> None:

        if len(self.__components) == 0:
            return

        tasks = [create_task(component.initialize()) for component in self.__components]
        done, _ = await wait(tasks, return_when=ALL_COMPLETED)

        for task in tasks:
            if exc := task.exception() is not None:
                await self._deinitialize(exc)

    async def _deinitialize(self, exception: Optional[Exception] = None) -> None:

        tasks = [
            create_task(component.deinitialize(exception)) for component in self.__components
            if issubclass(type(component.state), InitializedState)
        ]

        _, _ = await wait(tasks)

        if exception is not None:
            raise exception

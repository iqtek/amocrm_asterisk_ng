from typing import Optional

from glassio.initializable_components import AbstractInitializableComponent
from glassio.initializable_components import IState


__all__ = [
    "AsteriskNGComponent",
]


class AsteriskNGComponent(AbstractInitializableComponent):

    __slots__ = ()

    @property
    def state(self) -> IState:
        pass

    async def initialize(self) -> None:
        pass

    async def deinitialize(self, exception: Optional[Exception] = None) -> None:
        pass

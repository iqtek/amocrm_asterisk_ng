from ...core import IScenario
from ....domain import ICrm, ITelephony
from ....infrastructure import IEventBus


class ClassicScenario(IScenario):

    __slots__ = (
        "__event_bus",
        "__crm",
        "__telephony",
    )

    def __init__(
        self,
        event_bus: IEventBus,
        crm: ICrm,
        telephony: ITelephony
    ) -> None:
        self.__event_bus = event_bus
        self.__crm = crm
        self.__telephony = telephony

    @property
    def name(self) -> str:
        return "classic"

    async def upload(self) -> None:
        pass

    async def unload(self) -> None:
        pass

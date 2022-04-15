from amocrm_asterisk_ng.infrastructure import IEventBus
from amocrm_asterisk_ng.domain import ITelephony
from amocrm_asterisk_ng.domain import ICrm


__all__ = [
    "IScenario",
]


class IScenario:

    __slots__ = ()

    def __init__(
        self,
        event_bus: IEventBus,
        crm: ICrm,
        telephony: ITelephony,
    ) -> None:
        pass

    @property
    def name(self) -> str:
        raise NotImplementedError()

    async def upload(self) -> None:
        raise NotImplementedError()

    async def unload(self) -> None:
        raise NotImplementedError()

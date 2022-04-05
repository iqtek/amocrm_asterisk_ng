from asterisk_amocrm.infrastructure import ILogger
from ..ami_store import IAmiStore
from ......core.ami_manager import Event
from ......core.ami_manager import IAmiEventHandler


__all__ = [
    "NewCallerIdEventHandler",
]


class NewCallerIdEventHandler(IAmiEventHandler):

    __slots__ = (
        "__ami_store",
        "__logger",
    )

    __PHONE_TTL: int = 60 * 60 * 8

    def __init__(
        self,
        ami_store: IAmiStore,
        logger: ILogger,
    ) -> None:
        self.__ami_store = ami_store
        self.__logger = logger

    @classmethod
    def event_pattern(cls) -> str:
        return "NewCallerid"

    async def __call__(self, event: Event) -> None:

        channel = event["Channel"]
        phone_number = event["CallerIDNum"]

        try:
            await self.__ami_store.save_phone(
                channel=channel,
                phone=phone_number,
            )
        except Exception:
            self.__logger.debug(
                "NewCallerIdEventHandler: "
                f"Unable to set new phone '{phone_number}' number as "
                "it has already been set."
            )

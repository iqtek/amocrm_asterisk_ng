from amocrm_asterisk_ng.infrastructure import ILogger
from ..ami_store import IAmiStore
from ......core.ami_manager import Event
from ......core.ami_manager import IAmiEventHandler


__all__ = [
    "NewChannelEventHandler",
]


class NewChannelEventHandler(IAmiEventHandler):

    __slots__ = (
        "__ami_store",
        "__logger",
    )

    def __init__(
        self,
        ami_store: IAmiStore,
        logger: ILogger,
    ) -> None:
        self.__ami_store = ami_store
        self.__logger = logger

    @classmethod
    def event_pattern(cls) -> str:
        return "Newchannel"

    def __is_valid_phone(self, phone: str) -> bool:

        if len(phone) >= 9 and (phone[0] != "+" or phone[0] != "8"):
            return False
        return True

    async def __call__(self, event: Event) -> None:

        channel = event["Channel"]
        unique_id = event["Uniqueid"]
        linked_id = event["Linkedid"]

        await self.__ami_store.save_channel(
            channel=channel,
            unique_id=unique_id,
            linked_id=linked_id,
        )

        phone_number = event.get("CallerIDNum")

        if phone_number:
            if not self.__is_valid_phone(phone_number):
                self.__logger.warning(
                    "NewChannelEventHandler: "
                    "Phone invalid: "
                    f"phone: '{phone_number}' ]."
                )
                return
            try:
                await self.__ami_store.save_phone(
                    channel=channel,
                    phone=phone_number,
                )
            except Exception:
                await self.__ami_store.update_phone(
                    channel=channel,
                    phone=phone_number,
                )

            self.__logger.debug(
                "NewChannelEventHandler: "
                "Phone is forced to update: "
                f"[ channel: '{channel}' "
                f"new_phone: '{phone_number}' ]."
            )

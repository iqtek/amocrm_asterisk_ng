from datetime import datetime

from asterisk_ng.interfaces import ISetMuteTelephonyCommand
from asterisk_ng.interfaces import MuteStatusUpdateTelephonyEvent

from asterisk_ng.plugins.telephony.ami_manager import Action
from asterisk_ng.plugins.telephony.ami_manager import IAmiManager
from asterisk_ng.system.event_bus import IEventBus

from ...reflector import IReflector


__all__ = ["SetMuteTelephonyCommandImpl"]


class SetMuteTelephonyCommandImpl(ISetMuteTelephonyCommand):

    __slots__ = (
        "__ami_manager",
        "__reflector",
        "__event_bus",
    )

    def __init__(
        self,
        ami_manager: IAmiManager,
        reflector: IReflector,
        event_bus: IEventBus,
    ) -> None:
        self.__ami_manager = ami_manager
        self.__reflector = reflector
        self.__event_bus = event_bus

    async def __call__(
        self,
        phone_number: str,
        is_mute: bool,
    ) -> None:
        channel = await self.__reflector.get_channel_by_phone(phone=phone_number)

        action = Action(
            name="MuteAudio",
            parameters={
                "Channel": channel.name,
                "Direction": "in",
                "State": ("on" if is_mute else "off"),
            }
        )
        await self.__ami_manager.send_action(action)

        mute_status_update_telephony_event = MuteStatusUpdateTelephonyEvent(
            phone=phone_number,
            is_mute=is_mute,
            created_at=datetime.now()
        )

        await self.__event_bus.publish(mute_status_update_telephony_event)

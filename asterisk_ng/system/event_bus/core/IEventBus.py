from typing import Optional
from typing import Type

from .BaseEvent import BaseEvent
from .IEventBusSubscription import IEventBusSubscription
from .IEventHandler import IEventHandler


__all__ = ["IEventBus"]


class IEventBus:

    __slots__ = ()

    async def publish(self, event: BaseEvent) -> None:
        raise NotImplementedError()

    def subscribe(
        self,
        event_handler: IEventHandler,
        event_type: Optional[Type[BaseEvent]] = None
    ) -> IEventBusSubscription:
        raise NotImplementedError()

    def cancel_subscription(self, subscription: IEventBusSubscription) -> None:
        raise NotImplementedError()

    def cancel_all_subscriptions(self) -> None:
        raise NotImplementedError()

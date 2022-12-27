from typing import Optional
from typing import Type
from typing import TypeVar

from .BaseEvent import BaseEvent
from .IEventBusSubscription import IEventBusSubscription
from .IEventHandler import IEventHandler


__all__ = ["IEventBus"]


E = TypeVar('E', bound=BaseEvent)


class IEventBus:

    __slots__ = ()

    async def publish(self, event: BaseEvent) -> None:
        raise NotImplementedError()

    def subscribe(
        self,
        event_handler: IEventHandler[E],
        event_type: Optional[Type[E]] = None
    ) -> IEventBusSubscription[E]:
        raise NotImplementedError()

    def cancel_subscription(self, subscription: IEventBusSubscription) -> None:
        raise NotImplementedError()

    def cancel_all_subscriptions(self) -> None:
        raise NotImplementedError()

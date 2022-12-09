from asyncio import create_task
from collections import defaultdict

from typing import MutableMapping
from typing import MutableSequence
from typing import Optional
from typing import TypeVar
from typing import Type

from asterisk_ng.system.logger import ILogger

from .EventBusSubscriptionImpl import EventBusSubscriptionImpl

from ..core import BaseEvent
from ..core import IEventBus
from ..core import IEventBusSubscription
from ..core import IEventHandler


__all__ = ["EventBusImpl"]


E = TypeVar('E', bound=BaseEvent)


class EventBusImpl(IEventBus):

    __slots__ = (
        "__subscriptions",
        "__handlers",
        "__logger",
    )

    def __init__(
        self,
        logger: ILogger,
    ) -> None:
        self.__handlers: MutableMapping[Type[E], MutableSequence[IEventHandler[E]]] = defaultdict(list)
        self.__logger = logger

    async def __call_handler(self, event: E, handler: IEventHandler[E]) -> None:
        try:
            await handler(event)
        except Exception as exc:
            await self.__logger.error(
                f"Error during event processing event: `{event}`.",
                exception=exc,
            )

    async def publish(self, event: BaseEvent) -> None:
        handlers = self.__handlers.get(type(event), tuple())

        for handler in handlers:
            create_task(self.__call_handler(event, handler))
        await self.__logger.debug(
            f"Event published: {repr(event)}."
        )

    def subscribe(
        self,
        event_handler: IEventHandler,
        event_type: Optional[Type[BaseEvent]] = None,
    ) -> IEventBusSubscription:
        if event_type is None:
            try:
                event_type = event_handler.__call__.__annotations__["event"]
            except (KeyError, AttributeError):
                raise Exception("Handler does not have an event type annotation.")

        self.__handlers[event_type].append(event_handler)

        return EventBusSubscriptionImpl(
            event_type=event_type,
            event_handler=event_handler,
        )

    def cancel_subscription(self, subscription: IEventBusSubscription) -> None:
        try:
            self.__handlers[subscription.event_type].remove(subscription.event_handler)
        except KeyError:
            return

    def cancel_all_subscriptions(self) -> None:
        self.__handlers.clear()

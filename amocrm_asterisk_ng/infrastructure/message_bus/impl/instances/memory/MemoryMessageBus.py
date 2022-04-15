from asyncio import AbstractEventLoop
from asyncio import CancelledError
from asyncio import Future
from asyncio import PriorityQueue
from asyncio import Task

from functools import wraps
from itertools import cycle

from time import time

from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Iterator
from typing import MutableSequence
from typing import Optional

from amocrm_asterisk_ng.infrastructure import ILogger

from .MessageWrapper import MessageWrapper
from ....core import IConsumer
from ....core import InitializableMessageBus
from ....core import Message
from ....core import Properties


__all__ = [
    "MemoryMessageBus",
]


class MemoryMessageBus(InitializableMessageBus):

    __slots__ = (
        "__queue",
        "__consumer_added",
        "__event_loop",
        "__consumers",
        "__consumer_iterator",
        "__background_task",
        "__logger",
    )

    def __init__(
        self,
        queue: PriorityQueue,
        event_loop: AbstractEventLoop,
        logger: ILogger,
    ) -> None:
        self.__queue = queue
        self.__event_loop = event_loop
        self.__consumers: MutableSequence[IConsumer] = []
        self.__consumer_iterator: Iterator[IConsumer] = cycle(self.__consumers)
        self.__background_task: Optional[Task] = None
        self.__consumer_added: Future[Any] = Future()
        self.__logger = logger

    async def initialize(self) -> None:
        self.__background_task = self.__event_loop.create_task(
            self.__publishing_task(),
            name="MemoryMessageBus publishing task."
        )

    async def deinitialize(self) -> None:
        if self.__background_task is not None:
            self.__background_task.cancel()

    async def publish(
        self,
        message: Message,
        properties: Optional[Properties] = None
    ) -> None:
        properties = properties or Properties()
        message_wrapper = MessageWrapper(
            properties=properties,
            message=message,
        )
        self.__logger.debug(
            "MemoryMessageBus: "
            "message published "
            f"message_wrapper: `{message_wrapper}`."
        )
        await self.__queue.put(message_wrapper)

    async def add_consumer(self, consumer: IConsumer) -> None:
        self.__consumers.append(consumer)
        if not self.__consumer_added.done():
            self.__consumer_added.set_result(True)

    def __consumer_wrapper(
        self,
        consumer: IConsumer
    ) -> Callable[[MessageWrapper], Coroutine[Any, Any, None]]:
        @wraps(consumer)
        async def wrapper(
            message_wrapper: MessageWrapper,
        ) -> None:
            time_now = time()
            try:
                properties, message = message_wrapper.unwrap(time_now)
            except TimeoutError:
                self.__logger.debug(
                    "MemoryMessageBus: "
                    "message expired "
                    f"message_wrapper: `{message_wrapper}`."
                )
                return
            try:
                await consumer(
                    message=message,
                    properties=properties,
                )
            except Exception as e:
                self.__logger.warning(
                    "MemoryMessageBus: "
                    "message consumption error "
                    f"message_wrapper: `{message_wrapper}`."
                )
                self.__logger.exception(e)
                await self.publish(
                    message=message,
                    properties=properties,
                )
            else:
                self.__logger.debug(
                    "MemoryMessageBus: "
                    "message consumed "
                    f"message_wrapper: `{message_wrapper}`."
                )
        return wrapper

    async def __publish_message_wrapper(
        self,
        message_wrapper: MessageWrapper,
        consumer: IConsumer
    ) -> None:
        wrapped_consumer = self.__consumer_wrapper(consumer)
        self.__event_loop.create_task(
            wrapped_consumer(message_wrapper),
            name=f"MemoryMessageBus consumer: `{consumer}`."
        )

    async def __get_consumer(self) -> IConsumer:
        # Waiting for at least one consumer to be added.
        await self.__consumer_added
        return next(self.__consumer_iterator)

    async def __publishing_task(self) -> None:
        try:
            while True:
                message_wrapper = await self.__queue.get()
                consumer = await self.__get_consumer()
                await self.__publish_message_wrapper(message_wrapper, consumer)
        except CancelledError:
            while not self.__queue.empty():
                message_wrapper = await self.__queue.get()
                consumer = await self.__get_consumer()
                await self.__publish_message_wrapper(message_wrapper, consumer)

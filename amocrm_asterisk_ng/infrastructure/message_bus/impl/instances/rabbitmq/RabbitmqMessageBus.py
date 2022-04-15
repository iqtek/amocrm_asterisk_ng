from asyncio import AbstractEventLoop
from asyncio import BaseProtocol
from asyncio import BaseTransport
from asyncio import Lock
from typing import Optional

import aioamqp
from aioamqp.channel import Channel
from aioamqp.envelope import Envelope
from aioamqp.properties import Properties as AioamqpProperties

from amocrm_asterisk_ng.infrastructure import IGetCurrentAppVersionFunction
from amocrm_asterisk_ng.infrastructure import ILogger

from .properties_to_mapping import mapping_to_properties, properties_to_mapping
from .RabbitmqMessageBusConfig import RabbitmqMessageBusConfig

from ....core import IConsumer
from ....core import InitializableMessageBus
from ....core import Message
from ....core import Properties

__all__ = [
    "RabbitmqMessageBus",
]


class RabbitmqMessageBus(InitializableMessageBus):

    __slots__ = (
        "__config",
        "__lock",
        "__event_loop",
        "__get_app_version_function",
        "__transport",
        "__protocol",
        "__channel",
        "__logger",
    )

    def __init__(
        self,
        config: RabbitmqMessageBusConfig,
        get_app_version_function: IGetCurrentAppVersionFunction,
        event_loop: AbstractEventLoop,
        logger: ILogger,
    ) -> None:
        self.__config = config
        self.__lock: Lock = Lock()
        self.__get_app_version_function = get_app_version_function
        self.__event_loop = event_loop
        self.__logger = logger

        self.__transport: Optional[BaseTransport] = None
        self.__protocol: Optional[BaseProtocol] = None
        self.__channel: Optional[Channel] = None

    def __get_queue_name(self) -> str:
        current_version = str(self.__get_app_version_function())
        return f"{self.__config.queue_name}_v{current_version}"

    def __get_exchange_name(self) -> str:
        current_version = str(self.__get_app_version_function())
        return f"{self.__config.exchange_name}_v{current_version}"

    async def __connect(self) -> None:
        async with self.__lock:
            try:
                self.__transport, self.__protocol = await aioamqp.connect(
                    **self.__config.rabbitmq.dict(),
                    loop=self.__event_loop,
                )
                self.__channel: Channel = await self.__protocol.channel()
            except Exception as e:
                self.__logger.exception(e)
                raise Exception(
                    f"Fail to connect with: {self.__config.rabbitmq}."
                ) from e

    async def initialize(self) -> None:
        await self.__connect()
        await self.__channel.queue_declare(
            queue_name=self.__get_queue_name(),
            durable=True,
        )
        await self.__channel.exchange_declare(
            exchange_name=self.__get_exchange_name(),
            type_name=self.__config.exchange_type,
            durable=True,
        )
        await self.__channel.queue_bind(
            queue_name=self.__get_queue_name(),
            exchange_name=self.__get_exchange_name(),
            routing_key=self.__config.routing_key,
        )

    async def __disconnect(self) -> None:
        if self.__protocol is not None:
            await self.__protocol.close()
        if self.__transport is not None:
            self.__transport.close()

    async def deinitialize(self) -> None:
        await self.__disconnect()

    async def publish(
        self,
        message: Message,
        properties: Optional[Properties] = None
    ) -> None:
        exchange_name = self.__get_exchange_name()

        if properties is not None:
            dict_properties = properties_to_mapping(properties)
        else:
            dict_properties = {}

        try:
            await self.__channel.basic_publish(
                payload=message,
                exchange_name=exchange_name,
                routing_key=self.__config.routing_key,
                properties=dict_properties,
            )
        except Exception as e:
            raise Exception(f"Fail to publish message. {e}") from e

        self.__logger.debug(
            "RabbitmqMessageBus: "
            "Message published "
            f"payload: `{message}`, "
            f"properties: `{properties}`, "
            f"exchange_name: `{exchange_name}`, "
            f"routing_key: `{self.__config.routing_key}`."
        )

    async def add_consumer(self, consumer: IConsumer) -> None:

        async def consumer_wrapper(
            channel: Channel,
            body: bytes,
            envelope: Envelope,
            properties: AioamqpProperties,
        ) -> None:

            properties = mapping_to_properties(properties)

            nonlocal consumer
            try:
                await consumer(
                    message=body,
                    properties=properties,
                )
            except Exception as e:
                self.__logger.warning(
                    "RabbitmqMessageBus: "
                    "message processing error."
                    f"message: {body}. {e}"
                )
                self.__logger.exception(e)
                await channel.basic_reject(envelope.delivery_tag, requeue=True)
                return

            await channel.basic_client_ack(envelope.delivery_tag)
            self.__logger.debug(
                "RabbitmqMessageBus: "
                "message consumed "
                f"message: {body}."
            )

        await self.__channel.basic_consume(
            callback=consumer_wrapper,
            queue_name=self.__get_queue_name(),
        )

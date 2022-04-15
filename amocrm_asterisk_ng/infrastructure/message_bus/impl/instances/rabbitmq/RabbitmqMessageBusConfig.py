from typing import Literal

from pydantic import BaseModel

from .RabbitmqConfig import RabbitmqConfig


__all__ = [
    "RabbitmqMessageBusConfig",
]


class RabbitmqMessageBusConfig(BaseModel):
    rabbitmq: RabbitmqConfig = RabbitmqConfig()
    exchange_name: str = "asterisk_amocrm_ng_exchange"
    exchange_type: Literal["fanout", "direct", "topics", "headers"] = "direct"
    queue_name: str = "asterisk_amocrm_ng"
    routing_key: str = "asterisk_amocrm_ng"

from aioredis import Redis
from aioredis import from_url

from .RedisStorageConfigModel import RedisStorageConfigModel


__all__ = ["redis_connection_factory"]


def redis_connection_factory(config: RedisStorageConfigModel) -> Redis:
    try:
        redis = from_url(
            f"redis://{config.host}",
            port=config.port,
            db=config.database,
            password=config.password,
        )
    except Exception as exc:
        raise ConnectionError("Error of creating connection to Redis.") from exc
    return redis

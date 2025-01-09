import redis
from core.config import settings


def get_redis_client():
    """
    Establishes a connection to a Redis server.

    This function creates a Redis client using the connection settings from the
    application's configuration (such as host, port, and database index). The
    returned client can be used to interact with the Redis server for caching and
    other operations.

    Returns:
        redis.StrictRedis: A Redis client instance connected to the configured Redis server.

    Raises:
        redis.exceptions.ConnectionError: If there is an issue connecting to the Redis server.
    """
    return redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
    )

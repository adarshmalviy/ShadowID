import redis
from app.loggers import logger
from app.config import settings


class RedisService:
    _instance = None

    def __init__(self):
        if not RedisService._instance:
            try:
                # Initialize Redis connection
                self.redis = redis.Redis(
                    host=settings.redis_host,
                    port=settings.redis_port,
                    # password=settings.redis_password, # Optional, if Redis has password
                    db=settings.redis_db,
                    decode_responses=True,  # Optional, decode Redis responses
                )
                # Test Redis connection
                self.redis.ping()
                logger.info("Redis connection established successfully.")
                RedisService._instance = self
            except redis.ConnectionError as e:
                logger.error(f"Failed to connect to Redis: {str(e)}")
                raise e
        else:
            self.redis = RedisService._instance.redis

    @staticmethod
    def get_instance():
        if not RedisService._instance:
            RedisService()
        return RedisService._instance.redis

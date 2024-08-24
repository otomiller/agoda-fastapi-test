import json
from redis import Redis
from app.core.config import settings

redis = Redis.from_url(settings.REDIS_URL)

def get_cached_data(key: str):
    data = redis.get(key)
    return json.loads(data) if data else None

def set_cached_data(key: str, data: dict, expiration: int = 3600):
    redis.setex(key, expiration, json.dumps(data))
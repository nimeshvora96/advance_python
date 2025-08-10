import redis
import json
import os
from dotenv import load_dotenv
from typing import Optional, Any

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class CacheManager:
    @staticmethod
    def get(key: str) -> Optional[Any]:
        try:
            data = redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    @staticmethod
    def set(key: str, value: Any, expire: int = 30):
        try:
            redis_client.setex(key, expire, json.dumps(value, default=str))
        except Exception as e:
            print(f"Cache set error: {e}")
    
    @staticmethod
    def delete(key: str):
        try:
            redis_client.delete(key)
        except Exception as e:
            print(f"Cache delete error: {e}")
    
    @staticmethod
    def invalidate_pattern(pattern: str):
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
        except Exception as e:
            print(f"Cache invalidate error: {e}")

cache = CacheManager()
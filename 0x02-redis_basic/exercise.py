#!/usr/bin/env python3
"""writing strings to redis"""
import redis
import uuid
from typing import Callable, Optional

class cache:
    """A class cache using redis"""
    def __init__(self):
        """initialize the cache by creating a redis client
        and flushing the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data) -> str:
        """store the input data in Redis with a randomly generated key
        and return the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    
    def get(self, key: str, fn: Optional[Callable] = None):
        """Retrieve data from the cache using the provided key"""
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data
    
    def get_str(self, key: str):
        """Retrieve a string from the cache"""
        return self.get(key, fn=lambda d: d.decode("utf-8"))
    
    def get_int(self, key: str):
        """Retrieve an integer from the cache"""
        return self.get(key, fn=int)

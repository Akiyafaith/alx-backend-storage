#!/usr/bin/env python3
import redis
import uuid
"""writing strings to redis"""


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
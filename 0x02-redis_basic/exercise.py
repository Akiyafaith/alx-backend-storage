#!/usr/bin/env python3
"""writing strings to redis"""
from typing import Callable, Optional
from functools import wraps
import redis
import uuid


class cache:
    """A class cache using redis"""
    def __init__(self):
        """initialize the cache by creating a redis client
        and flushing the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def count_calls(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = f"{self.__class__.__name__}.{method.__name__}"
            self._redis.incr(key)
            return method(self, *args, **kwargs)

        return wrapper
    
    def call_history(method: Callable) -> Callable:
        """Decorator to store the history of inputs and outputs"""
        def wrapper(self, *args, **kwargs):
            input_key = "{}:inputs".format(method.__qualname__)
            output_key = "{}:outputs".format(method.__qualname__)

            self._redis.rpush(input_key, str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush(output_key, result)

            return result

        return wrapper

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

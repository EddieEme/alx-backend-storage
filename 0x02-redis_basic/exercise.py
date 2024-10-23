#!/usr/bin/env python3
"""
Cache class module using Redis with type conversion
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    """
    Cache class to handle Redis operations
    """
    def __init__(self):
        """
        Initialize the Cache instance with a Redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key
        Args:
            data: The data to be stored (can be str, bytes, int, or float)
        Returns:
            str: The randomly generated key used to store the data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, 
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Get data from Redis and convert it to the desired format
        Args:
            key: The key to look up in Redis
            fn: Optional function to convert the data
        Returns:
            The data in the desired format, or None if the key doesn't exist
        """
        data = self._redis.get(key)
        if data is None:
            return None
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """
        Get a string value from Redis
        Args:
            key: The key to look up in Redis
        Returns:
            str: The value as a string, or None if the key doesn't exist
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Get an integer value from Redis
        Args:
            key: The key to look up in Redis
        Returns:
            int: The value as an integer, or None if the key doesn't exist
        """
        return self.get(key, int)
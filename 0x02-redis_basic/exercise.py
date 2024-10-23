#!/usr/bin/env python3
"""
Cache class module using Redis
"""
import redis
import uuid
from typing import Union


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
        # Generate a random key using uuid
        key = str(uuid.uuid4())
        
        # Store the data in Redis
        self._redis.set(key, data)
        
        return key

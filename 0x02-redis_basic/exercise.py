#!/usr/bin/env python3
"""
Cache class module using Redis with call counting, history tracking and replay
"""
import redis
import uuid
import functools
from typing import Union, Callable, Optional


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function
    Args:
        method: The method to display history for
    """
    # Get the Redis instance from the class
    redis_instance = method.__self__._redis
    method_name = method.__qualname__

    # Get the number of calls from count_calls decorator
    calls = redis_instance.get(method_name)
    calls = int(calls) if calls else 0

    print(f"{method_name} was called {calls} times:")

    # Get inputs and outputs from call_history decorator
    inputs = redis_instance.lrange(f"{method_name}:inputs", 0, -1)
    outputs = redis_instance.lrange(f"{method_name}:outputs", 0, -1)

    # Print each call with input and output
    for inp, out in zip(inputs, outputs):
        print(f"{method_name}(
            *{inp.decode('utf-8')}) -> {out.decode('utf-8')}")


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times methods of Cache class are called
    Args:
        method: The method to be decorated
    Returns:
        Callable: The wrapped method
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count and calls the method
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    Args:
        method: The method to be decorated
    Returns:
        Callable: The wrapped method
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores input and output history
        """
        input_list = f"{method.__qualname__}:inputs"
        output_list = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_list, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_list, str(output))

        return output
    return wrapper


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

    @call_history
    @count_calls
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

    def get(self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
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

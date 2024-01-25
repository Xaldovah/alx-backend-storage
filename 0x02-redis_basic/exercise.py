#!/usr/bin/env python3
"""Module containing the Cache class for storing data in Redis"""

import redis
import uuid
import functools
from typing import Union, Callable


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        - method (Callable): The method to be decorated.

        Returns:
            - Callable: The decorated method
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count and calls
        the original method.

        Args:
            - self: The instance of the class.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

            Returns:
                - The result of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """
    Cache class for storing data in Redis.

    Methods:
        - __init__: Initializes Redis client and flushes the Redis database
        - store: Generates a random key, stores the input data in Redis,
                 and returns the key.
    """

    def __init__(self):
        """
        Initializes the Cache instance.

        Creates a private variable _redis as an instance of the Redis
        client and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis and return the generated key.

        Args:
            - data (Union[str, bytes, int, float]): The data to be stored.

            Returns:
                - str: The generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, None]:
        """
        Retrieve data from Redis using the given key
        and apply a conversion function if provided.
        """
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve a string from Redis using the given key."""
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve an integer from Redis using the given key."""
        return self.get(key, fn=int)

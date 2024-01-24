#!/usr/bin/env python3
"""Module containing the Cache class for storing data in Redis"""

import redis
import uuid
from typing import Union, Callable


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

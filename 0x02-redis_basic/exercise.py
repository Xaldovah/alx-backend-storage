#!/usr/bin/env python3
"""Module containing the Cache class for storing data in Redis"""

import redis
import uuid
from typing import Union


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

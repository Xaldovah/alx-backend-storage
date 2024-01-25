#!/usr/bin/env python3
"""Module containing the Cache class for storing data in Redis"""

import redis
import uuid
import functools
from typing import Union, Callable


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a
    particular function
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that retrieves the output

        Args:
            - self: The instance of the class.
            - *args: Variable length argument list.
            - **kwargs: Arbitrary keyword arguments.

            - The result of the original method
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output
    return wrapper


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

    @call_history
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


def replay(method: Callable) -> None:
    """
    Replay the stored history of inputs and outputs for a given method.

    Args:
        - method (Callable): The method for which the history is replayed.

        Returns:
            - None
    """
    cache = Cache()
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(input_key, 0, -1)
    outputs = cache._redis.lrange(output_key, 0, -1)

    call_count = cache._redis.get(method.__qualname__)
    if call_count is None:
        print(f"{method.__qualname__} was never called.")
    else:
        print(f"{method.__qualname__} was called {int(call_count)} times:")
        for input_data, output_data in zip(inputs, outputs):
            print(
                    f"{method.__qualname__}*({input_data.decode()}) -> "
                    f"{output_data.decode()}"
            )

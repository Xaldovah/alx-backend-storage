#!/usr/bin/env python3
"""Module for retrieving and caching web pages with access tracking."""

import functools
import requests
import redis
import time
from typing import Callable


redis_client = redis.Redis()


def track_access(method: Callable) -> Callable:
    """Decorator to track the number of times a function
    is called for a given URL."""

    @functools.wraps(method)
    def wrapper(url: str) -> str:
        key = f"count:{url}"
        redis_client.incr(key)  # Increment access count in Redis
        return method(url)

    return wrapper


def cache_result(expiration: int = 10) -> Callable:
    """Decorator to cache the result of a function
    for a given expiration time."""

    def decorator(method: Callable) -> Callable:
        @functools.wraps(method)
        def wrapper(url: str) -> str:
            cache_key = f"cached_page:{url}"
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode("utf-8")  # Return cached result

            result = method(url)
            redis_client.setex(cache_key, expiration, result)  # Cache result
            return result

        return wrapper

    return decorator


@track_access
@cache_result(expiration=10)  # Cache for 10 seconds
def get_page(url: str) -> str:
    """Retrieves the HTML content of a given URL,
    handling caching and tracking.

    Args:
        url (str): The URL of the page to retrieve.

        Returns:
            str: The HTML content of the url

            Raises:
                requests.HTTPError: If the request fails with an
                error status code.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for error status codes
    time.sleep(2)
    return response.text

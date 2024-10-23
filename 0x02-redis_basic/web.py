#!/usr/bin/env python3
"""In this tasks, we will implement a get_page function
(prototype: def get_page(url: str) -> str:). The core of
the function is very simple. It uses the requests module
to obtain the HTML content of a particular URL and returns it.
Start in a new file named web.py and do not reuse the code
written in exercise.py.
Inside get_page track how many times a particular URL was
accessed in the key "count:{url}" and cache the result with
an expiration time of 10 seconds.
Tip: Use http://slowwly.robertomurray.co.uk to simulate
a slow response and test your caching."""


import redis
import requests
from functools import wraps


r = redis.Redis()


def url_access_count(method):
    """decorator for get_page function"""
    @wraps(method)
    def wrapper(url):
        """wrapper function"""
        # Increment the access counter
        r.incr(f"count:{url}")

        # Check if we have cached content
        cached_response = r.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')

        # Get new content and cache it
        html_content = method(url)
        r.setex(f"cached:{url}", 10, html_content)

        return html_content
    return wrapper


@url_access_count
def get_page(url: str) -> str:
    """obtain the HTML content of a particular URL"""
    return requests.get(url).text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')

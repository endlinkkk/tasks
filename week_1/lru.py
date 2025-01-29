import unittest.mock
from functools import wraps
from typing import Callable


def _lru_wrapper(func: Callable, maxsize: int = 128):
    memo = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(memo) >= maxsize:
            key_ = next(iter(memo.keys()))
            del memo[key_]
        key_ = frozenset([*args, *kwargs.values()])
        if memo.get(key_):
            result = memo[key_]
        else:
            result = func(*args, **kwargs)
            memo[frozenset(key_)] = result
        return result

    return wrapper


def lru_cache(maxsize=128):
    if callable(maxsize):
        user_function, maxsize = maxsize, 128
        wrapper = _lru_wrapper(user_function, maxsize)
        return wrapper
    elif isinstance(maxsize, int):
        if maxsize < 0:
            maxsize = 0
    elif maxsize is not None:
        raise TypeError("Expected first argument to be an integer, a callable, or None")

    def decorated_function(func):
        return _lru_wrapper(func, maxsize)

    return decorated_function


@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == "__main__":
    assert sum(1, 2) == 3
    assert sum(3, 4) == 7

    assert multiply(1, 2) == 2
    assert multiply(3, 4) == 12

    assert sum_many(1, 2, c=3, d=4) == 10

    mocked_func = unittest.mock.Mock()
    mocked_func.side_effect = [1, 2, 3, 4]

    decorated = lru_cache(maxsize=2)(mocked_func)
    assert decorated(1, 2) == 1
    assert decorated(1, 2) == 1
    assert decorated(3, 4) == 2
    assert decorated(3, 4) == 2
    assert decorated(5, 6) == 3
    assert decorated(5, 6) == 3
    assert decorated(1, 2) == 4
    assert mocked_func.call_count == 4

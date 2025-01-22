import unittest.mock
from functools import wraps

def lru_cache(*args, **kwargs):
    memo = {}
    if kwargs.get('maxsize'):
        maxsize = kwargs['maxsize']
        def wrapper1(func):
            @wraps(func)
            def wrapper2(*args_f, **kwargs_f):
                if len(memo) >= maxsize:
                    key_ = next(iter(memo.keys()))
                    del memo[key_]
                key_ = frozenset([*args_f, *kwargs_f.values()])
                if memo.get(key_):
                    result = memo[key_]
                else:
                    result = func(*args_f, **kwargs_f)
                    memo[frozenset(key_)] = result

                return result 
            return wrapper2
        return wrapper1
    else:
        func = args[0]
        @wraps(func)
        def wrapper(*args_f, **kwargs_f):
            key_ = frozenset([*args_f, *kwargs_f.values()])
            if memo.get(key_):
                result = memo[key_]
            else:
                result = func(*args_f, **kwargs_f)
                memo[frozenset(key_)] = result

            return result 
        return wrapper



@lru_cache
def sum(a: int, b: int) -> int:
    return a + b


@lru_cache
def sum_many(a: int, b: int, *, c: int, d: int) -> int:
    return a + b + c + d


@lru_cache(maxsize=3)
def multiply(a: int, b: int) -> int:
    return a * b


if __name__ == '__main__':
    
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

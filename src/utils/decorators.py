from functools import wraps

DEBUG_STRING_WRAPPER = "DEBUG: {}"


def protect(func):
    """ Декоратор, который защищает всё от неожиданного сваливания """
    import traceback

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(DEBUG_STRING_WRAPPER.format('CRITICAL ERROR\n' + traceback.format_exc()))

    return wrapper


def benchmark(func):
    """ Декоратор, который время замеряет """
    from time import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        res = func(*args, **kwargs)
        delta_time = time() - start_time
        print(
            DEBUG_STRING_WRAPPER.format("function '{}' complete in {:.2f} ms".format(func.__name__, delta_time * 1000)))
        return res

    return wrapper


def counter(func):
    """ Декоратор, который считает вызовы конкретной функции """

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print(DEBUG_STRING_WRAPPER.format("function '{0}' was called {1} time(s)".format(func.__name__, wrapper.count)))
        return func(*args, **kwargs)

    wrapper.count = 0
    return wrapper


def logging(func):
    """ Декоратор, который логи делает """
    n = 60

    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        msg = "{}\nName: {}\nArgs: {}\nKwargs: {}\nResult: {}\n{}".format(
            "=" * (n - len(DEBUG_STRING_WRAPPER) + 2), func.__name__, args, kwargs, res, "=" * n)
        print(DEBUG_STRING_WRAPPER.format(msg))
        return res

    return wrapper

import time


def protect(func):
    """
    Декоратор, который защищает всё от неожиданного сваливания
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("EXCEPTION {} IN {}".format(e, func.__name__))

    return wrapper


def timetest(func):
    """
    Декоратор, который время замеряет
    """
    def timed(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        print("Name: {}\nArgs: {}\nKwargs: {}\nTime: {:.4f} s\n{}".format(
            func.__name__, args, kwargs, end_time - start_time, "="*40))
        return result

    return timed

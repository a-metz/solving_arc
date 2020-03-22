import signal
from functools import wraps


class Timeout(Exception):
    pass


def handler(*args):
    raise Timeout()


def timeout(time):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(time)
            try:
                return func(*args, **kwargs)
            except Timeout:
                print("timeout")
            return None

        return wrapper

    return decorator

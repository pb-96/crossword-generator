from functools import wraps
from datetime import datetime
from time import mktime, localtime, sleep

# 3600 seconds which is one hour times 24 which is one day
ONE_HOUR = 60 * 60 * 24


def get_local_time() -> datetime:
    local_time = mktime(localtime())
    as_current_time = datetime.fromtimestamp(local_time)
    return as_current_time


def repeat_every_day(hour: int, minute: int, second: int):
    def decorator_func(func):
        @wraps(func)
        def time_wrapper(*args, **kwargs):
            while True:
                delta = datetime(hour=hour, minute=minute, second=second)
                delta.day = delta.day + 1
                now = datetime.now()
                while now < delta:
                    sleep(ONE_HOUR)
                    now = datetime.now()
                func(args, kwargs)

        return time_wrapper

    return decorator_func

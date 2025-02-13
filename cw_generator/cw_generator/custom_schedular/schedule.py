from functools import wraps
from datetime import datetime
from time import mktime, localtime


def get_local_time() -> datetime:
    local_time = mktime(localtime())
    as_current_time = datetime.fromtimestamp(local_time)
    return as_current_time


def repeat_every_day(hour: int, minute: int, second: int):

    def decorator_func(func):
        @wraps(func)
        def time_wrapper(*args, **kwargs):
            
            func(args, kwargs)
        time_wrapper.next_send = None
        return time_wrapper

    return decorator_func

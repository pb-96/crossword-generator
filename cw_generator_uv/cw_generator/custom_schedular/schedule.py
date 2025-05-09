from functools import wraps
from datetime import datetime, time, timedelta
from time import mktime, localtime, sleep


def get_local_time() -> datetime:
    local_time = mktime(localtime())
    as_current_time = datetime.fromtimestamp(local_time)
    return as_current_time


def repeat_every_day(hour: int, minute: int, second: int):
    def decorator_func(func):
        @wraps(func)
        def time_wrapper(*args, **kwargs):
            while True:
                now = datetime.now()
                today_target = datetime.combine(now.date(), time(hour, minute, second))

                if now >= today_target:
                    # If we've already passed the target time today, schedule for tomorrow
                    today_target += timedelta(days=1)

                sleep_seconds = (today_target - now).total_seconds()
                sleep(sleep_seconds)

                func(*args, **kwargs)

        return time_wrapper

    return decorator_func

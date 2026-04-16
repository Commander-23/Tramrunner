import pytz
from datetime import datetime
from .vvo_time_conv import vvo_time_conv

def diff_to_now(expiery_time):
    if isinstance(expiery_time, str):
        timestamp = vvo_time_conv(expiery_time).astimezone(pytz.utc)
    elif isinstance(expiery_time, datetime):
        timestamp = expiery_time.astimezone(pytz.utc)
    else:
        raise ValueError(f"should be str or datetime: {expiery_time}")
    utc = datetime.now(pytz.utc)
    delta = timestamp - utc
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}h{minutes}m"
    elif minutes > 0:
        return f"{minutes}m{seconds}s"
    else:
        return f"{seconds}s"
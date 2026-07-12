from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
import pytz
import re
def vvo_time_conv(dvb_time_noformat: str) -> datetime:
    """
        sign = 1 if tz_str[0] == "+" else -1
        tz_hours = int(tz[1:3])
        tz_minutes = int(tz[3:5])
        offset = timedelta(tz_hours, tz_minutes) * sign
        tzinfo = timezone(offset)
    """

    PATTERN = re.compile(r"/Date\((?P<ms>-?\d+)(?P<tz>[+-]\d{4})?\)/")
    dvb_time = PATTERN.match(dvb_time_noformat)
    if not dvb_time:
        raise ValueError(f"Invalid DVB Timestamp: {dvb_time_noformat!r}")
    timestamp_seconds = int(dvb_time.group("ms")) / 1000

    timezone_str = dvb_time.group("tz")



    if timezone_str:
        timezone_sign = 1 if timezone_str[0] == "+" else -1
        timezone_hours = int(timezone_str[1:3]) 
        timezone_minutes = int(timezone_str[3:5])
        timezone_offset = timedelta(hours=timezone_hours, minutes=timezone_minutes) * timezone_sign
        timezone_info = timezone(timezone_offset)
    else:
        timezone_info = timezone.utc

    timestamp = datetime.fromtimestamp(timestamp_seconds, tz=timezone_info)
    return timestamp 

@dataclass
class VvoTime:
    raw: str
    milliseconds: int
    tz_offset: str | None
    timestamp: datetime

    PATTERN = re.compile(r"/Date\((?P<ms>-?\d+)(?P<tz>[+-]\d{4})?\)/")

    def __post_init__(self):
        if self.tz_offset:
            timezone_sign = 1 if self.tz_offset[0] == "+" else -1
            timezone_hours = int(self.tz_offset[1:3]) 
            timezone_minutes = int(self.tz_offset[3:5])
            timezone_offset = timedelta(hours=timezone_hours, minutes=timezone_minutes) * timezone_sign
            timezone_info = timezone(timezone_offset)
        else:
            timezone_info = timezone.utc
        self.timestamp = datetime.fromtimestamp(self.milliseconds / 1000, tz=timezone_info)

    @classmethod
    def from_string(cls, input: str):
        match = cls.PATTERN.match(input)

        if not match:
            raise ValueError(f"Invalid DVB Timestamp: {input!r}")
        return cls(
            raw=input,
            milliseconds=int(match.group("ms")),
            tz_offset=match.group("tz"),
            timestamp=None
        )
    def format_6digits(self):
        return self.timestamp.astimezone().strftime("%H:%M:%S")

    def diff_to_now(self):
        delta = self.timestamp - datetime.now(pytz.utc)
        total_seconds = int(delta.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            return f"{hours}h{minutes}m"
        elif minutes > 0:
            return f"{minutes}m{seconds}s"
        else:
            return f"{seconds}s"

if __name__ == "__main__":
    func_out = vvo_time_conv("/Date(1767662520000+0100)/")
    print(f"converted timestamp:        {func_out}")
    print(f"time diff to current time:  {func_out}")
    print(f"current Time:               {datetime.now()}")
from datetime import datetime, timedelta, timezone
import re
def vvo_timestamp_to_datetime_class(dvb_time_noformat: str) -> datetime:
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

if __name__ == "__main__":
    func_out = vvo_timestamp_to_datetime_class("/Date(1767662520000+0100)/")
    print(f"converted timestamp:        {func_out[0]}")
    print(f"time diff to current time:  {func_out[1]}")
    print(f"current Time:               {datetime.now()}")
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

    return datetime.fromtimestamp(timestamp_seconds, tz=timezone_info)


    #human_readable_time = datetime.fromtimestamp(int(dvb_time[6:-7])/1000)
    #
    #tz_offset_hh = int(dvb_time[19:-4])
    #tz_offset_mm = int(dvb_time[22:-2])
    #timezone_delta = timedelta(hours=tz_offset_hh, minutes=tz_offset_mm)
    #return human_readable_time, timezone_delta

if __name__ == "__main__":
    func_out = vvo_timestamp_to_datetime_class("/Date(1764662520000+0100)/")
    time_now = datetime.now(timezone.utc)
    time_diff = time_now - func_out.astimezone(timezone.utc)    

    print(f"\n" + "#"*50 + "\n")
    print(f"func_out:   {func_out.isoformat(timespec="hours")}")
    print(f"time_now:   {time_now.isoformat()}")
    print(f"time_diff:  {time_diff}")
    print(f"\n" + "#"*50 + "\n")
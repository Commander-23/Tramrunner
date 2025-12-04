from datetime import datetime, timedelta
import re
def vvo_timestamp_to_datetime_class(dvb_time_noformat: str):
    """
    Pattern


        sign = 1 if tz_str[0] == "+" else -1
        tz_hours = int(tz[1:3])
        tz_minutes = int(tz[3:5])
        offset = timedelta(tz_hours, tz_minutes) * sign
        tzinfo = timezone(offset)


    """
    PATTERN = re.compile(r"/Date\((?P<ms>-?\d+)(?P<tz>[+-]\d{4})?\)/")
    dvb_time = PATTERN.match(dvb_time_noformat)
    timestamp_ms = int(dvb_time.group("ms"))
    timezone_str = dvb_time.group("tz")


    timezone_sign = 1 if timezone_str[0] == "+" else -1
    timezone_hours = int(timezone_str[1:3]) 
    timezone_minutes = int(timezone_str[3:5])
    timezone_offset = timedelta(timezone_hours, timezone_minutes) * timezone_sign
    
    
    #out = {timestamp_ms, timezone_str, timezone_sign, timezone_hours, timezone_minutes}
    #return  out


    human_readable_time = datetime.fromtimestamp(int(dvb_time[6:-7])/1000)
    
    tz_offset_hh = int(dvb_time[19:-4])
    tz_offset_mm = int(dvb_time[22:-2])
    timezone_delta = timedelta(hours=tz_offset_hh, minutes=tz_offset_mm)
    return human_readable_time, timezone_delta

if __name__ == "__main__":
    print(vvo_timestamp_to_datetime_class("/Date(1764662530512+0100)/"))

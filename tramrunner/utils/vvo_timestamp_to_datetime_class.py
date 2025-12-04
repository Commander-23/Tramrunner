from datetime import datetime, timedelta
import re
def vvo_timestamp_to_datetime_class(dvb_time: str):
    """
    Pattern

        PATTERN = re.compile(r"/Date\((?P<ms>-?\d+)(?P<tz>[+-]\d{4})?\)/")
        m = PATTERN.match(dvb_timestamp)
        ms = int(m.group("ms"))
        tz = m.group("tz")
        
        sign = 1 if tz_str[0] == "+" else -1
        tz_hours = int(tz[1:3])
        tz_minutes = int(tz[3:5])
        offset = timedelta(tz_hours, tz_minutes) * sign
        tzinfo = timezone(offset)


    """



    # /Date(1753482300000-0000)/
    PATTERN = re.compile(r"/Date\((?P<ms>-?\d+)(?P<tz>[+-]\d{4})?\)/")
    matched_str = PATTERN.match(dvb_time)




    human_readable_time = datetime.fromtimestamp(int(dvb_time[6:-7])/1000)
    
    tz_offset_hh = int(dvb_time[19:-4])
    tz_offset_mm = int(dvb_time[22:-2])
    timezone_delta = timedelta(hours=tz_offset_hh, minutes=tz_offset_mm)
    
    return human_readable_time, timezone_delta
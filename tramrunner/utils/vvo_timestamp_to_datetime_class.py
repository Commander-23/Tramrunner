from datetime import datetime, timedelta

def vvo_timestamp_to_datetime_class(input: str):
    # /Date(1753482300000-0000)/
    human_readable_time = datetime.fromtimestamp(int(input[6:-7])/1000)
    
    tz_offset_hh = int(input[19:-4])
    tz_offset_mm = int(input[22:-2])
    timezone_delta = timedelta(hours=tz_offset_hh, minutes=tz_offset_mm)
    
    return human_readable_time, timezone_delta
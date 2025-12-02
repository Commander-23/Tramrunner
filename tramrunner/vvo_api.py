import requests
import json
from datetime import datetime, timedelta
from api import query_vvo_api
from api import vvo_pointfinder as vvo_api_pointfinder
from api import vvo_departure_monitor as vvo_api_departure_monitor
from api import vvo_trip_details as vvo_api_trip_details
from api import vvo_query_trip as vvo_api_query_trip
from api import vvo_route_changes as vvo_api_route_changes
from api import vvo_lines as vvo_api_lines


def vvo_timestamp_to_datetime_class(input: str):
    # /Date(1753482300000-0000)/
    human_readable_time = datetime.fromtimestamp(int(input[6:-7])/1000)
    
    tz_offset_hh = int(input[19:-4])
    tz_offset_mm = int(input[22:-2])
    timezone_delta = timedelta(hours=tz_offset_hh, minutes=tz_offset_mm)
    
    return human_readable_time, timezone_delta

def get_stop_id_from_pointfinder(query: str) -> str:
    """
    query the VVO pointfinder API to get the stop ID for a given query.

    Args:
        query (str): The query to search for in the VVO API.

    Returns:
        str: The stop ID for the given query.
    """
    api_response = vvo_api_pointfinder(query=query, limit=10, stopsOnly=True, regionalOnly=True)
    if api_response is not None and 'Points' in api_response:
        return api_response['Points'][0].split('|')[0]
    else:
        print("Failed to retrieve stop ID from pointfinder.")
        return None

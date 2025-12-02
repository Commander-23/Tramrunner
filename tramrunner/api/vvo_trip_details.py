from api import query_vvo_api

def vvo_trip_details(tripid: str, time: str, stopid: str, mapdata: bool = False):
    """
    Get Details about the stations involved in a trip.
    Arguments:
        tripid : The "id" received from the departure monitor (Departures[*].Id)
        time : The current time as unix timestamp plus timezone. Has to be in the future. Most likely from a departure monitor response (Departures[*].RealTime / Departures[*].ScheduledTime).
        stopid : ID of a stop in the route. This stop will be marked with Position=Current in the response.
        mapdata : Unknown. Seems to have no effect.
    """

    defaulturl = "https://webapi.vvo-online.de/dm/trip"
    if not tripid or not time or not stopid:
        raise ValueError("Trip ID, time, and stop ID cannot be empty.")

    query_params = {
        "tripid": tripid,
        "time": time,
        "stopid": stopid,
        "mapdata": mapdata
    }

    return query_vvo_api(defaulturl, None, query_params)

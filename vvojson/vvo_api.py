import requests
from static_vvo import write_to_json, web_get_json, load_geojson, search_geojson

headers = {
    "Content-Type": "application/json",
    "charset": "utf-8"
    }





def get_stop_info(query: str) -> dict:
    """
    Fetches information about a specific stop using its ID.
    
    Args:
        stop_id (str): The ID of the stop to fetch information for.
        
    Returns:
        dict: A dictionary containing stop information.
    """

    base_url = "https://webapi.vvo-online.de/tr/pointfinder"
    headers = {
    "Content-Type": "application/json",
    "charset": "utf-8"
    }
    
    params = {
        "query": query,
        "stopsOnly": True
    }

    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    if response.status_code == 200:
        return response.json()  # parse JSON response
    else:
        print(f"Request failed with status {response.status_code}: {response.text}")


def vvo_api_pointfinder(query: str, limit: int = 0, stopsOnly: bool = False, regionalOnly: bool = False, stopShortcuts: bool = False) -> None:
    """
    Find stops based certain parameters.
    Arguments:
        query : Search query.
        limit : The maximum number of results to return.
        stopsOnly : If True, only return stops.
        regionalOnly : If True, restrict results to regional stops.
        stopShortcuts : If True, include stop shortcuts in the results.
    """
    defaulturl = "https://webapi.vvo-online.de/tr/pointfinder"
    if not query:
        raise ValueError("Query parameter cannot be empty.")

    params = {
        "query": query,
        "limit": limit,
        "stopsOnly": stopsOnly,
        "regionalOnly": regionalOnly,
        "stopShortcuts": stopShortcuts
    }
    print(params)



def vvo_api_departure_monitora(stopid: str, limit: int = 0, time: str = '' , isarrival: bool = False, shorttermchanges: bool = False, mot: list = None) -> None:
    """
    List out upcoming departures from a stop id.
    Arguments:   
        stopid : ID of the stop	
        limit : Maximum number of results
        time : ISO8601 timestamp, e.g. 2017-02-22T15:40:26Z
        isarrival : Is the time specified above supposed to be interpreted as arrival or departure time?
        shorttermchanges : unknown in this context
        mot : Allowed modes of transport, see below
            Currently accepted modes of transport are `Tram`, `CityBus`, `IntercityBus`, `SuburbanRailway`, `Train`, `Cableway`, `Ferry`, `HailedSharedTaxi`.    
    """
    
    defaulturl = "https://webapi.vvo-online.de/dm"
    if not stopid:
        raise ValueError("Stop ID cannot be empty.")
    if mot is None:
        mot = ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"]

    params = {
        "stopid": stopid,
        "limit": limit,
        "time": time,
        "isarrival": isarrival,
        "shorttermchanges": shorttermchanges,
        "mot": mot
    }



def vvo_api_trip_details(tripid: str, time: str, stopid: str, mapdata: bool = False) -> None:
    """
    Get Details about the stations involved in a trip.
    Arguments:
        tripid : The "id" received from the departure monitor (Departures[*].Id)
        time : The current time as unix timestamp plus timezone. Has to be in the future. Most likely from a departure monitor response (Departures\[\*\].RealTime / Departures\[\*\].ScheduledTime).
        stopid : ID of a stop in the route. This stop will be marked with Position=Current in the response.
        mapdata : Unknown. Seems to have no effect.
    """

    defaulturl = "https://webapi.vvo-online.de/dm/trip"
    if not tripid or not time or not stopid:
        raise ValueError("Trip ID, time, and stop ID cannot be empty.")

    params = {
        "tripid": tripid,
        "time": time,
        "stopid": stopid,
        "mapdata": mapdata
    }



def vvo_api_query_trip(origin: str, destination: str, shorttermchanges: bool = False, time: str = "", isArrivalTime: bool = False) -> None:
    """
    Query how to get from station "Hauptbahnhof" (stopid 33000028) to station "Bahnhof Neustadt" (stopid 33000016).
    Arguments:
        origin : stopid of start station
        destination : stopid of destination station
        shorttermchanges : unknown in this context
        time : ISO8601 timestamp, e.g. 2017-02-22T15:40:26Z
        isArrivalTime : Is the time specified above supposed to be interpreted as arrival or departure time?
    """
    defaulturl = "https://webapi.vvo-online.de/tr/trips"
    headers["X-Requested-With"] = "de.dvb.dvbmobil"
    if not origin or not destination:
        raise ValueError("Origin or destination cannot be empty.")

    params = {
        "origin": origin,
        "destination": destination,
        "shorttermchanges": shorttermchanges,
        "time": time,
        "isArrivalTime": isArrivalTime
    }



def vvo_api_route_changes(shortterm: bool = True) -> None:
    """
    Get information about route changes because of construction work or such.
    Arguments:
        shortterm : unknown. I diffed the output with and without -> no diff
    """
    defaulturl = "https://webapi.vvo-online.de/rc"

    params = {"shortterm": shortterm}



def vvo_api_lines(stopid: str) -> None:
    """
    Get informatin about wich lines do service a stop.
    """
    if not stopid:
        raise ValueError("Stop ID cannot be empty.")
    
    params = {"stopid": stopid}
    pass


if 1 == 1:
    vvo_api_pointfinder("Bahnhof Mitte")

if 1 != 1:
    #
    data = web_get_json(url=None,nolines=True)
    #print(data)
    search_key = 'name'
    search_value = 'Bahnhof Mitte'
    results = search_geojson(data, search_key, search_value)
    #print(results)
    print(results[0]['properties']['id'])

    api_result = get_stop_info(results[0]['properties']['id'])
    write_to_json(api_result, "/home/cmdr/dev-py/files/pointfinder.json")

    
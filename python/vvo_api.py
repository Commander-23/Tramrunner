import requests
import json
from static_vvo import write_to_json, web_get_json, load_geojson, search_geojson

headers = {
    "Content-Type": "application/json",
    "charset": "utf-8"
    }


def vvo_api_pointfinder(query: str, limit: int = 0, stopsOnly: bool = False, regionalOnly: bool = False, stopShortcuts: bool = False) -> dict:
    """
    Find stops based certain parameters.
    Arguments:
        query, lim
        query : Search query.
        limit : The maximum number of results to return.
        stopsOnly : If True, only return stops.
        regionalOnly : If True, restrict results to regional stops.
        stopShortcuts : If True, include stop shortcuts in the results.
    Returns:
        {'PointStatus': 'Identified', 'Status': {'Code': 'Ok'}, 'Points': ['33000313|||Räcknitzhöhe|5655709|4622355|0||'], 'ExpirationTime': '/Date(1753115786301+0200)/'}
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
    # {'query': 'Räcknitzhöhe', 'limit': 10, 'stopsOnly': True, 'regionalOnly': False, 'stopShortcuts': False}


    try:
        response = requests.get(defaulturl, params=params, headers=headers, timeout=5, verify=True) 
        if response.status_code == 200:
            content = json.loads(response.content.decode('utf-8'))
            # response {'PointStatus': 'Identified', 'Status': {'Code': 'Ok'}, 'Points': ['33000313|||Räcknitzhöhe|5655709|4622355|0||'], 'ExpirationTime': '/Date(1753115786301+0200)/'}
            
            output = content['Points'][0].split('|')
            # outputs the first point in the list, e.g. ['33000313', '', 'Räcknitzhöhe', '5655709', '4622355', '0', '']
            
            return output
        else:
            raise requests.HTTPError('HTTP Status: {}'.format(response.status_code))    
    except requests.RequestException as e:
        print(f"Failed to access VVO pointfinder. Request Exception", e)
        response = None
    
    if response is None:
        return None



def vvo_api_departure_monitor(stopid: str, limit: int = 0, time: str = '' , isarrival: bool = False, shorttermchanges: bool = False, mot: list = None) -> None:
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
        time : The current time as unix timestamp plus timezone. Has to be in the future. Most likely from a departure monitor response (Departures[*].RealTime / Departures[*].ScheduledTime).
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
    defaulturl = "https://webapi.vvo-online.de/stt/lines"
    if not stopid:
        raise ValueError("Stop ID cannot be empty.")
    
    params = {"stopid": stopid}
    
    try:
        response = requests.get(defaulturl, params=params, headers=headers, timeout=5, verify=True) 
        if response.status_code == 200:
            content = json.loads(response.content.decode('utf-8'))
            # response {'PointStatus': 'Identified', 'Status': {'Code': 'Ok'}, 'Points': ['33000313|||Räcknitzhöhe|5655709|4622355|0||'], 'ExpirationTime': '/Date(1753115786301+0200)/'}
            
            #output = content['Points'][0].split('|')
            # outputs the first point in the list, e.g. ['33000313', '', 'Räcknitzhöhe', '5655709', '4622355', '0', '']
            
            return content
        else:
            raise requests.HTTPError('HTTP Status: {}'.format(response.status_code))    
    except requests.RequestException as e:
        print(f"Failed to access VVO pointfinder. Request Exception", e)
        response = None
    
    if response is None:
        return None


if 1 != 1:
    print(vvo_api_pointfinder("Räcknitzhöhe", limit=10, stopsOnly=True))

    userinput = input("Enter a stop name or ID: ")
    stop_id = vvo_api_pointfinder(userinput, limit=10, stopsOnly=True)[0]
    print(stop_id)
    lines = vvo_api_lines(stop_id)
    print(lines)

if 1 != 1:
    #
    
    data = web_get_json(url=None,nolines=True)
    #print(data)
    search_key = 'name'
    search_value = 'Bahnhof Mitte'
    results = search_geojson(data, search_key, search_value)
    #print(results)
    print(results[0]['properties']['id'])

    
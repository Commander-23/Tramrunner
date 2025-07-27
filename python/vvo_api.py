import requests
import json
from datetime import datetime, timedelta

default_headers = {
    "Content-Type": "application/json",
    "charset": "utf-8"
    }

def query_vvo_api(url: str, headers: dict, params: dict = None) -> dict:
    """
    Query the VVO API to get information about stops, departures, and trips.
    """
    if not url:
        raise ValueError("URL cannot be empty.")
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5, verify=True) 
        if response.status_code == 200:
            content = json.loads(response.content.decode('utf-8'))
            
            output = content #content['Points'][0].split('|')
            # outputs the first point in the list, e.g. ['33000313', '', 'Räcknitzhöhe', '5655709', '4622355', '0', '']
            
            return output
        else:
            raise requests.HTTPError('HTTP Status: {}'.format(response.status_code))    
    except requests.RequestException as e:
        print(f"Failed to access VVO pointfinder. Request Exception", e)
        response = None
    
    if response is None:
        return None


def vvo_api_pointfinder(query: str, limit: int = 0, stopsOnly: bool = False, regionalOnly: bool = False, stopShortcuts: bool = False):
    """
    Find stops based certain parameters.
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
        response = requests.get(defaulturl, params=params, headers=default_headers, timeout=5, verify=True) 
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

def vvo_api_departure_monitor(stopid: str, limit: int = 0, time: str = '' , isarrival: bool = False, shorttermchanges: bool = False, mot: list = None):
    """
    Get the departures from a stop by stopid.
    """
    """
    Response:
        {
            "Name": "Räcknitzhöhe",
            "Status": {"Code": "Ok"},
            "Place": "Dresden",
            "ExpirationTime": "/Date(1753468523932+0200)/",
            "Departures": [
                {
                    "Id": "voe:21085: :H:j25",
                    "DlId": "de:vvo:21-85",
                    "LineName": "85",
                    "Direction": "Löbtau Süd",
                    "Platform": {"Name": "2", "Type": "Platform"},
                    "Mot": "CityBus",
                    "RealTime": "/Date(1753468500000-0000)/",
                    "ScheduledTime": "/Date(1753468560000-0000)/",
                    "State": "InTime",
                    "RouteChanges": ["23520", "23448"],
                    "Diva": {"Number": "21085", "Network": "voe"},
                    "CancelReasons": [],
                    "Occupancy": "Unknown"
                },
                {
                ...
                }
            ]
        } 
    """
    
    defaulturl = "https://webapi.vvo-online.de/dm"
    if not stopid:
        raise ValueError("Stop ID cannot be empty.")
    if mot is None:
        mot = ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"]

    query_params = {
        "stopid": stopid,
        "limit": limit,
        "time": time,
        "isarrival": isarrival,
        "shorttermchanges": shorttermchanges,
        "mot": mot
    }

    return query_vvo_api(defaulturl, default_headers, query_params)

def vvo_api_trip_details(tripid: str, time: str, stopid: str, mapdata: bool = False):
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

    return query_vvo_api(defaulturl, default_headers, query_params)

def vvo_api_query_trip(origin: str, destination: str, shorttermchanges: bool = False, time: str = "", isArrivalTime: bool = False):
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
    default_headers["X-Requested-With"] = "de.dvb.dvbmobil"
    
    if not origin or not destination:
        raise ValueError("Origin or destination cannot be empty.")

    query_params = {
        "origin": origin,
        "destination": destination,
        "shorttermchanges": shorttermchanges,
        "time": time,
        "isArrivalTime": isArrivalTime
    }

    return query_vvo_api(defaulturl, default_headers, query_params)

def vvo_api_route_changes(shortterm: bool = True):
    """
    Get information about route changes because of construction work or such.
    Arguments:
        shortterm : unknown. I diffed the output with and without -> no diff
    """
    defaulturl = "https://webapi.vvo-online.de/rc"

    query_params = {"shortterm": shortterm}

    return query_vvo_api(defaulturl, default_headers, query_params)

def vvo_api_lines(stopid: str):
    """
    Get informatin about wich lines do service a stop.
    """
    defaulturl = "https://webapi.vvo-online.de/stt/lines"
    if not stopid:
        raise ValueError("Stop ID cannot be empty.")
    
    query_params = {"stopid": stopid}
    
    return query_vvo_api(defaulturl, default_headers, query_params)


def vvo_timestamp_to_datetime_class(input: str):
    # /Date(1753482300000-0000)/
    human_readable_time = datetime.fromtimestamp(int(input[6:-7])/1000)
    
    tz_offset_hh = int(input[19:-4])
    tz_offset_mm = int(input[22:-2])
    timezone_delta = timedelta(hours=tz_offset_hh, minutes=tz_offset_mm)
    
    return human_readable_time, timezone_delta
from api import query_vvo_api

def vvo_query_trip(origin: str, destination: str, shorttermchanges: bool = False, time: str = "", isArrivalTime: bool = False):
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
    headers = {
        "content-Type": "application/json",
        "charset": "utf-8",
        "X-Requested-With": "de.dvb.dvbmobil"

    }
    
    if not origin or not destination:
        raise ValueError("Origin or destination cannot be empty.")

    query_params = {
        "origin": origin,
        "destination": destination,
        "shorttermchanges": shorttermchanges,
        "time": time,
        "isArrivalTime": isArrivalTime
    }

    return query_vvo_api(defaulturl, headers, query_params)['Routes']

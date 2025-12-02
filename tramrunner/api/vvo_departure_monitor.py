from api import query_vvo_api

def vvo_departure_monitor(stopid: str, limit: int = 0, time: str = '' , isarrival: bool = False, shorttermchanges: bool = False, mot: list = None):
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

    return query_vvo_api(defaulturl, None, query_params)

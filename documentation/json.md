# Json Format

```json
    {
    'type': 'Feature', 
    'properties': {'number': 'de:14612:1', 'nameWithCity': 'Dresden Bahnhof Mitte', 'name': 'Bahnhof Mitte', 'city': 'Dresden'},
    'geometry': {'type': 'Point', 'coordinates': [x:y]},  
    'Lines': [{'Operator': 'DVB', 'Route': 'Dresden Prohlis Gleisschleife-Dresden Leutewitz', 'Vehicle': 'Straßenbahn', 'TripID': 'voe:11001: :H:j25', 'LineNr': '1'}]
    }
```

A List of Dictionaries in Dictionary

`{'foo':'str', 'bar':[{},{}]}`

```json
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
    ]
}
```

# Overview of departure monitor Response

```json Request-overview
{
    "Name": "Hauptbahnhof",
    "Status": {
        "Code": "Ok"
    },
    "Place": "Dresden",
    "ExpirationTime": "/Date(1764662530512+0100)/",
    "Departures": [
        {}, {}, {}
    ]
}
```


```json Departure-Overview
{
    "Id": "voe:11008: :H:j25",
    "DlId": "de:vvo:11-8",
    "LineName": "8",
    "Direction": "Südvorstadt",
    "Platform": {"Name": "4", "Type": "Platform"},
    "Mot": "Tram",
    "RealTime": "/Date(1764662520000-0000)/",
    "ScheduledTime": "/Date(1764662340000-0000)/",
    "State": "Delayed",
    "RouteChanges": ["24546"],
    "Diva": {"Number": "11008","Network": "voe"},
    "CancelReasons": [],
    "Occupancy": "Unknown"
}
```

## Identification

interesting:
- `LineName`
- `Direction`

uninteresting:
- `Id`
- `DlId`
- `Diva`

## Departure location & Mode of transport

- `Platform`
- `Mot`
- `Occupancy`

## Delay's and Changes

interesting:
- `RealTime`
- `ScheduledTime`
- `State`
- `RouteChanges`
- `CancelReasons`


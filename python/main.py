from vvo_api import vvo_api_pointfinder, vvo_api_departure_monitor, vvo_api_trip_details, vvo_api_query_trip, vvo_api_lines, vvo_timestamp_to_datetime_class
from static_vvo import write_to_json, web_get_json, load_geojson, search_geojson
from datetime import datetime, timedelta


"""
stopid = 0
lines = vvo_api_lines(stop_id)
pointfinder = vvo_api_pointfinder(stop_id, limit=10, stopsOnly=True, regionalOnly=False, stopShortcuts=False)
trip_details =None #vvo_api_trip_details(tripid='', time='', stop_id = stop_id, mapdata=False)
query_trip = None #vvo_api_query_trip(origin='', destination='', shorttermchanges=False, time='', isArrivalTime=False)
lines = vvo_api_lines(stop_id)
"""
"""
write_to_json(departures, "/home/cmdr/tramrunner/files/api_response_departures.json")
write_to_json(pointfinder, "/home/cmdr/tramrunner/files/api_response_pointfinder.json")
write_to_json(trip_details, "/home/cmdr/tramrunner/files/api_response_trip_details.json")
write_to_json(query_trip, "/home/cmdr/tramrunner/files/api_response_query_trip.json")
write_to_json(lines, "/home/cmdr/tramrunner/files/api_response_lines.json")
"""

def line_info_tui():
    userinput = "rac"#input("Enter a stop name or ID: ")
    stop_id = vvo_api_pointfinder(userinput, limit=10, stopsOnly=True)[0]
    mot = ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"]
    departures = vvo_api_departure_monitor(stop_id, limit=10, time='', isarrival=False, shorttermchanges=False, mot = mot)
    print(departures)

    query_trip = vvo_api_query_trip("ztz", "bue", shorttermchanges=False, time='', isArrivalTime=False)

    write_to_json(query_trip, "/home/cmdr/tramrunner/files/api_response_query_trip.json")
    write_to_json(departures, "/home/cmdr/tramrunner/files/api_response_departures.json")
    
def departure_monitor_tui():
    userinput = input("Enter a stop name or ID: ")
    stop_id = vvo_api_pointfinder(userinput, limit=10, stopsOnly=True)[0]
    mot = ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"]
    departures = vvo_api_departure_monitor(stop_id, limit=10, time='', isarrival=False, shorttermchanges=False, mot = mot)

    print("\n"*3)
    print(f"Station Name: {departures['Name']}")
    print(f"City: {departures['Place']}")

    Expiery_Time = vvo_timestamp_to_datetime_class(departures['ExpirationTime'])[0]
    TimeZone = vvo_timestamp_to_datetime_class(departures['ExpirationTime'])[1]
    print(f"Expiery Time: {Expiery_Time + TimeZone}")

    # Print the departure times
    print("\nDeparture Times:")
    for departure in departures['Departures']:
        print(f"- {departure['LineName']} to {departure['Direction']}")
        if 'RealTime' in departure:
            print(f"   Real-time Departure: {vvo_timestamp_to_datetime_class(departure['RealTime'])[0] + TimeZone}")
        print(f"   Scheduled Departure: {vvo_timestamp_to_datetime_class(departure['ScheduledTime'])[0] + TimeZone}")
        print(f"   Platform: {departure['Platform']['Name']}")





#departure_monitor_tui()
line_info_tui()
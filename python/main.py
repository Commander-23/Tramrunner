from vvo_api import * #vvo_api_pointfinder, vvo_api_departure_monitor, vvo_api_trip_details, vvo_api_query_trip, vvo_api_lines, vvo_timestamp_to_datetime_class, get_stop_id_from_pointfinder
from static_vvo import write_to_json, web_get_json, load_geojson, search_geojson
from datetime import datetime, timedelta

# define filepaths for output files
path_departures = "/home/cmdr/tramrunner/files/api_response_departures.json"
path_pointfinder = "/home/cmdr/tramrunner/files/api_response_pointfinder.json"
path_trip_details = "/home/cmdr/tramrunner/files/api_response_trip_details.json"
path_query_trip = "/home/cmdr/tramrunner/files/api_response_query_trip.json"
path_lines = "/home/cmdr/tramrunner/files/api_response_lines.json"

"""
stopid = 0
lines = vvo_api_lines(stop_id)
pointfinder = vvo_api_pointfinder(stop_id, limit=10, stopsOnly=True, regionalOnly=False, stopShortcuts=False)
trip_details =None #vvo_api_trip_details(tripid='', time='', stop_id = stop_id, mapdata=False)
query_trip = None #vvo_api_query_trip(origin='', destination='', shorttermchanges=False, time='', isArrivalTime=False)
lines = vvo_api_lines(stop_id)
"""


def line_info_tui(start, destination):
    #userinput = "rac"#input("Enter a stop name or ID: ")
    #stop_id = vvo_api_pointfinder(userinput, limit=10, stopsOnly=True)[0]
    #mot = ["Tram"]
    #departures = vvo_api_departure_monitor(stop_id, limit=10, time='', isarrival=False, shorttermchanges=False, mot = mot)
    #print(departures)
    #TimeZone = vvo_timestamp_to_datetime_class(departures['ExpirationTime'])[1]

    query_trip = vvo_api_query_trip(start, destination, shorttermchanges=False, time='', isArrivalTime=False)
    regular_stops = query_trip["Routes"][0]['PartialRoutes'][0]['RegularStops']
    
    print("\nZschernitz --> Bühlau")
    for stop in regular_stops:
        print(f"{stop['Name']}")
        print(f"    Departure Time: {vvo_timestamp_to_datetime_class(stop['DepartureTime'])[0]}\n")# + TimeZone}")
        print(f"    Arrival Time: {vvo_timestamp_to_datetime_class(stop['ArrivalTime'])[0]}\n")# + TimeZone}\n")
        #print("")

    #write_to_json(query_trip, path_query_trip)
    #write_to_json(departures, path_departures)
    
def departure_monitor_tui(userinput=None):
    """
    Run the departure monitor application.
    
    Args:
        userinput (str, optional): The stop name or ID to query. Defaults to None.
    """
    if userinput is not None:
        stop_id = get_stop_id_from_pointfinder(userinput)
    else:
        print("Please provide a stop name or ID.")
        return

    mot = ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"]
    
    try:
        api_response = vvo_api_departure_monitor(stop_id, limit=10)
        if 'Departures' in api_response:
            print("\nStation Name:", api_response['Name'])
            print("City:", api_response['Place'])

            expiration_time = vvo_timestamp_to_datetime_class(api_response['ExpirationTime'])[0]
            print("Expiery Time:", expiration_time.strftime("%H:%M:%S"))

            # Print the departure times
            for departure in api_response['Departures']:
                if 'RealTime' in departure:
                    real_departure_time = vvo_timestamp_to_datetime_class(departure['RealTime'])[0]
                    print(f"- {departure['LineName']} to {departure['Direction']}:\t\tReal-time: {real_departure_time.strftime("%H:%M")}")
                else:
                    scheduled_departure_time = vvo_timestamp_to_datetime_class(departure['ScheduledTime'])[0]
                    print(f"- {departure['LineName']} to {departure['Direction']}:\t\tScheduled: {scheduled_departure_time.strftime("%H:%M")}")

    except Exception as e:
        print("\aAn Error Occured")
        print(e)



    """
    #userinput = input("Enter a stop name or ID: ")
    stop_id = vvo_api_pointfinder(userinput, limit=10, stopsOnly=True)[0]
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
            print(f"   Real-time Departure: {vvo_timestamp_to_datetime_class(departure['RealTime'])[0]}")# + TimeZone}")
        print(f"   Scheduled Departure: {vvo_timestamp_to_datetime_class(departure['ScheduledTime'])[0]}")# + TimeZone}")
        print(f"   Platform: {departure['Platform']['Name']}")
"""



start = input("Starting location: ")
destination = input("Destination: ")
if destination == "":
    departure_monitor_tui(start)
else:    #vvo_api_query_trip(origin=start, destination=destination, shorttermchanges=False, time='', isArrivalTime=False)
    line_info_tui(start, destination)
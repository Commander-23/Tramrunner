
from vvo_api import * #vvo_api_pointfinder, vvo_api_departure_monitor, vvo_api_trip_details, vvo_api_query_trip, vvo_api_lines, vvo_timestamp_to_datetime_class, get_stop_id_from_pointfinder
from static_vvo import write_to_json, web_get_json, load_geojson, search_geojson
from datetime import datetime, timedelta
import os
import sys


# define filepaths for output files
script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
path_pointfinder = script_directory + "/cached_results/api_response_pointfinder.json"
path_departure_monitor = script_directory + "/cached_results/api_response_departures.json"
path_trip_details = script_directory + "/cached_results/api_response_trip_details.json"
path_query_trip = script_directory + "/cached_results/api_response_query_trip.json"
path_lines = script_directory + "/cached_results/api_response_lines.json"

def fill_json_data():
    """
    fills in the reference documents
    """
    write_to_json(vvo_api_pointfinder(query="Hauptbahnhof", limit=3), path_pointfinder)
    write_to_json(vvo_api_departure_monitor(stopid="33000028", limit=3), path_departure_monitor)
    #write_to_json(vvo_api_trip_details(tripid='', time='', stop_id = ''), path_trip_details)
    write_to_json(vvo_api_query_trip(origin="33000262", destination="33003815"), path_query_trip)
    write_to_json(vvo_api_lines(stopid="33000028"), path_lines)

fill_json_data()
def line_info_tui(start, destination):
    """
    """
    
    start_stop_id = get_stop_id_from_pointfinder(start)
    destination_stop_id = get_stop_id_from_pointfinder(destination)

    print(start_stop_id)
    print(destination_stop_id)



    query_trip = vvo_api_query_trip(start_stop_id, destination_stop_id, shorttermchanges=False, time='', isArrivalTime=False)
    #regular_stops = query_trip["Routes"][0]['PartialRoutes'][0]['RegularStops']
    # mot_chain = query

    write_to_json(query_trip, path_query_trip)

    print(partial_route_digger(query_trip))

    for route in query_trip['Routes']:
        #print("\n")
        print(f"\nRouteId: {route['RouteId']}")
        for chain in route['MotChain']:
            print(f"- {chain['Name']}\t{chain['Direction']}")
              
    return
#    for trip in query_trip['Routes'][0]['PartialRoutes']:
#        print(stop[])
#


    print("\nZschernitz --> Bühlau")
    for stop in regular_stops:
        print(f"{stop['Name']}")
        print(f"    Departure Time: {vvo_timestamp_to_datetime_class(stop['DepartureTime'])[0]}\n")# + TimeZone}")
        print(f"    Arrival Time: {vvo_timestamp_to_datetime_class(stop['ArrivalTime'])[0]}\n")# + TimeZone}\n")
        #print("")

    #write_to_json(query_trip, path_query_trip)
    #write_to_json(departures, path_departures)

def partial_route_digger(path_query_trip):
    
    # where to find
    # foo: route1, route2, just the diffren results
    # bar: tram_ride1, foothpath2, pices of the whole route with route info in them
    #
    #
    # jsonobj --> Routes[foo] --> Route_pieces[bar] --> RegularStops[n] --> {DataId:}
    
    for route in path_query_trip['Routes']:
        for partial_route in route['PartialRoutes']:
            for stops in partial_route['RegularStops']:
                print("__")

    


    return

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
        api_response = vvo_api_departure_monitor(stop_id, limit=18)
        if 'Departures' in api_response:
            print("\nStation Name:", api_response['Name'])
            print("City:", api_response['Place'])

            expiration_time = vvo_timestamp_to_datetime_class(api_response['ExpirationTime'])[0]
            print("Expiery Time:", expiration_time.strftime("%H:%M:%S"))

            # Print the departure times
            for departure in api_response['Departures']:
                if 'RealTime' in departure:
                    real_departure_time = vvo_timestamp_to_datetime_class(departure['RealTime'])[0]
                    print(f"- {departure['LineName']}\t{departure['Direction']}:\t\tReal-time: {real_departure_time.strftime("%H:%M")}")
                else:
                    scheduled_departure_time = vvo_timestamp_to_datetime_class(departure['ScheduledTime'])[0]
                    print(f"- {departure['LineName']}\t{departure['Direction']}:\t\tScheduled: {scheduled_departure_time.strftime("%H:%M")}")

    except Exception as e:
        print("\aAn Error Occured")
        print(e)

start = input("Starting location: ")
destination = input("Destination: ")
if destination == "":
    departure_monitor_tui(start)
else:    #vvo_api_query_trip(origin=start, destination=destination, shorttermchanges=False, time='', isArrivalTime=False)
    line_info_tui(start, destination)

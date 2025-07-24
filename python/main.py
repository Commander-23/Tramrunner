from vvo_api import vvo_api_pointfinder, vvo_api_departure_monitor, vvo_api_trip_details, vvo_api_query_trip, vvo_api_lines
from static_vvo import write_to_json, web_get_json, load_geojson, search_geojson

#print(vvo_api_pointfinder("Räcknitzhöhe", limit=10, stopsOnly=True))

userinput = input("Enter a stop name or ID: ")
stop_id = vvo_api_pointfinder(userinput, limit=10, stopsOnly=True)[0]
lines = vvo_api_lines(stop_id)

mot = ["Tram", "CityBus", "IntercityBus", "SuburbanRailway", "Train", "Cableway", "Ferry", "HailedSharedTaxi"]

pointfinder = vvo_api_pointfinder(stop_id, limit=10, stopsOnly=True, regionalOnly=False, stopShortcuts=False)
departure = vvo_api_departure_monitor(stop_id, limit=10, time='', isarrival=False, shorttermchanges=False, mot = mot)
trip_details = None #vvo_api_trip_details(tripid='', time='', stop_id = stop_id, mapdata=False)
query_trip = None #vvo_api_query_trip(origin='', destination='', shorttermchanges=False, time='', isArrivalTime=False)
lines = vvo_api_lines(stop_id)



write_to_json(pointfinder, "/home/cmdr/tramrunner/files/pointfinder.json")
write_to_json(departure, "/home/cmdr/tramrunner/files/departures.json")
write_to_json(trip_details, "/home/cmdr/tramrunner/files/api_response_trip_details.json")
write_to_json(query_trip, "/home/cmdr/tramrunner/files/api_response_query_trip.json")
write_to_json(lines, "/home/cmdr/tramrunner/files/api_response_lines.json")



print(stop_id)
#print(lines)
#print(departure)['Departures']
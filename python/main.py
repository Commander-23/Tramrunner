from vvo_api import vvo_api_pointfinder, vvo_api_departure_monitor, vvo_api_trip_details, vvo_api_query_trip, vvo_api_lines

#print(vvo_api_pointfinder("Räcknitzhöhe", limit=10, stopsOnly=True))

userinput = input("Enter a stop name or ID: ")
stop_id = vvo_api_pointfinder(userinput, limit=10, stopsOnly=True)[0]
print(stop_id)
lines = vvo_api_lines(stop_id)
#print(lines)
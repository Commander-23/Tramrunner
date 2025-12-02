import utils
import api
def save_response_to_file():
    utils.write_to_json(api.vvo_pointfinder(query="Hauptbahnhof", limit=3), "response_pointfinder.json")
    utils.write_to_json(api.vvo_departure_monitor(stopid="33000028", limit=3), "response_departure_monitor.json")
    #utils.write_to_json(api.vvo_trip_details(tripid='', time='', stop_id = ''), "response_trip_details.json")
    utils.write_to_json(api.vvo_query_trip(origin="33000262", destination="33003815"), "response_query_trip.json")
    utils.write_to_json(api.vvo_lines(stopid="33000028"), "response_lines.json")

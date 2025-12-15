import utils, api

stop_id_rac = utils.get_stop_id_from_pointfinder("rac")
stop_id_hbf = utils.get_stop_id_from_pointfinder("hbf")
stop_id_len = utils.get_stop_id_from_pointfinder("len")
stop_id_biw = utils.get_stop_id_from_pointfinder("biw")


def trip_info_tui(query_trip_data):
    for trip in query_trip_data:
        #print("mot chain:")
        #for mot_chain_item in trip["MotChain"]:
            #print(mot_chain_item["Name"])

        rtid = trip["RouteId"]
        print(f"\n\nRoute nr: {rtid}")
        for partial_route in trip["PartialRoutes"]:
            partial_mot = partial_route["Mot"]
            mot_type = partial_mot.get("ProductName", "mot_type")
            mot_name = partial_mot.get("Name", "mot_name")
            mot_direction = partial_mot.get("Direction", "???")
            header = (
                f"{mot_type} {mot_name} → {mot_direction} "
                f"({partial_route['Duration']} min)"
            )
            print(header)
            print("│")

            if partial_route['Mot']['Type'] != "Footpath":
                stops = partial_route["RegularStops"]
            else: stops = None
            for i, stop in enumerate(stops):
                is_last = i == len(stops) - 1
                connector = "└─" if is_last else "├─"

                time = utils.vvo_timestamp_to_datetime_class(stop["DepartureTime"]).astimezone().strftime('%H:%M')
                name = stop["Name"]
                platform = stop.get("Platform", {}).get("Name", "?")
                print(f"{connector} {time} {name} [P{platform}]")

            #print(partial_route["PartialRouteId"])

if __name__ == "__main__":
    #stop1 = utils.get_stop_id_from_pointfinder(input("Start: "))
    #stop2 = utils.get_stop_id_from_pointfinder(input("Dest:  "))
    trip_data = api.vvo_query_trip(stop_id_rac, stop_id_hbf)
    utils.write_to_json(trip_data, "response_query_trip.json")
    trip_info_tui(trip_data)
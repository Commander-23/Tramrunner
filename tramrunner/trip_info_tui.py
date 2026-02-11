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
        print(f"\n\nRoute nr: {rtid} {"-"*15}")
        for partial_route in trip["PartialRoutes"]:
            partial_mot = partial_route["Mot"]
            mot_type = partial_mot.get("Type", "mot_type")
            mot_name = partial_mot.get("Name", "mot_name")
            mot_direction = partial_mot.get("Direction", "???")
            partial_route_duration = partial_route.get("Duration", "???")
            header = (
                f"{mot_type} {mot_name} → {mot_direction} "
                f"({partial_route_duration} min)"
            )
            print(f"\n{header}")
            #stops = partial_route["RegularStops"]
            stops = partial_route.get("RegularStops", "[]")
            for i, stop in enumerate(stops):
                is_last = i == len(stops) - 1
                connector = "└─" if is_last else "├─"
                try:
                    time = utils.vvo_time_conv(stop["DepartureTime"]).astimezone().strftime('%H:%M')
                    name = stop["Name"]
                    stop_place = stop.get("Place", "???")
                    platform = stop.get("Platform", {}).get("Name", "?")
                except: time = "xx:xx"; name = "noName"; platform = "noName"
                print(f"{connector} {time} {name}, {stop_place}")

            #print(partial_route["PartialRouteId"])

if __name__ == "__main__":
    userin_start = input("Start: ")
    userin_stop = input("Dest:  ")
    if userin_start == "":
        userin_start = "August-Bebel-Straße, Radeberg"
    if userin_stop == "":
        userin_stop = "Siedlung, Wilsdruff"

    #stop1 = utils.get_stop_id_from_pointfinder(input("Start: "))
    #stop2 = utils.get_stop_id_from_pointfinder(input("Dest:  "))
    stop1 = utils.get_stop_id_from_pointfinder(userin_start)
    stop2 = utils.get_stop_id_from_pointfinder(userin_stop)
    trip_data = api.vvo_query_trip(stop1, stop2)
    utils.write_to_json(trip_data, "response_query_trip.json")
    trip_info_tui(trip_data)
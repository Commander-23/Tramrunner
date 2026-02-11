import api
import utils


def line_info_tui(start, destination):
    """
    """
    
    start_stop_id = utils.get_stop_id_from_pointfinder(start)
    destination_stop_id = utils.get_stop_id_from_pointfinder(destination)

    print(start_stop_id)
    print(destination_stop_id)



    query_trip = api.vvo_query_trip(start_stop_id, destination_stop_id, shorttermchanges=False, time='', isArrivalTime=False)
    #regular_stops = query_trip["Routes"][0]['PartialRoutes'][0]['RegularStops']
    # mot_chain = query


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
        print(f"    Departure Time: {vvo_time_conv(stop['DepartureTime'])[0]}\n")# + TimeZone}")
        print(f"    Arrival Time: {vvo_time_conv(stop['ArrivalTime'])[0]}\n")# + TimeZone}\n")
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


start = input("Starting location: ")
destination = input("Destination: ")
line_info_tui(start, destination)

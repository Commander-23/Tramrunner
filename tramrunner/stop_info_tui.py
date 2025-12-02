import utils, api

def stop_info_tui(userinput:str=None):
    if userinput is not None:
        stopid = utils.get_stop_id_from_pointfinder(userinput)
    else:
        print("Please provide a stop name or ID.")
        return None
    
    try:
        departure_monitor_response = api.vvo_departure_monitor(stopid, limit=15)
        station_name = departure_monitor_response['Name']
        station_city = departure_monitor_response['Place']
        expiration_time = utils.vvo_timestamp_to_datetime_class(departure_monitor_response['ExpirationTime'])[0]
        expiration_time_human = expiration_time.strftime("%H:%M:%S")

        output_lines = [
            f"\nAbfahrten für '{station_name}':\nUngültig in {expiration_time_human}",
            f"{'Linie':<8}{'Richtung':<30}{'Ankunft':<10}",
            "-" * 48
        ]
        for departure in departure_monitor_response['Departures']:
            line_number = departure.get('LineName')
            line_direction = departure.get('Direction')
            arrival_real_time = utils.vvo_timestamp_to_datetime_class(departure.get('RealTime'))[0].strftime("%H:%M:%S")
            arrival_scheduled_time = utils.vvo_timestamp_to_datetime_class(departure.get('ScheduledTime'))[0].strftime("%H:%M:%S")

            output_lines.append(f"{line_number:<8}{line_direction:<30}{arrival_real_time:<10}")
        return "\n".join(output_lines)
    except Exception as e:
        print("\aAnError Occured")
        print(e)
    return None


if __name__ == "__main__":
    userinput = input("Haltestelle: ")
    print(stop_info_tui(userinput))
import utils, api
from datetime import datetime

def stop_info_tui(userinput:str=None):
    if userinput is not None:
        stopid = utils.get_stop_id_from_pointfinder(userinput)
    else:
        print("Please provide a stop name or ID.")
        return None
    
    #try:
    departure_monitor_response = api.vvo_departure_monitor(stopid, limit=15)
    station_name = departure_monitor_response['Name']
    station_city = departure_monitor_response['Place']
    expiration_time = utils.vvo_timestamp_to_datetime_class(departure_monitor_response['ExpirationTime'])
    expiration_time_human = expiration_time.strftime("%H:%M:%S")

    output_lines = [
        f"\nAbfahrten für '{station_name}':\nUngültig in {expiration_time_human}",
        f"{'Linie':<8}{'Richtung':<30}{'Ankunft':<10}",
        "-" * 48
    ]
    for departure in departure_monitor_response['Departures']:
        line_number = departure.get('LineName')
        line_direction = departure.get('Direction')

        arrival_scheduled_time = utils.vvo_timestamp_to_datetime_class(departure.get('ScheduledTime')).astimezone().strftime("%H:%M:%S")
        
        arrival_display = arrival_scheduled_time

        if departure.get('RealTime'):
            arrival_real_time = utils.vvo_timestamp_to_datetime_class(departure.get('RealTime'))
            time_now = datetime.now(arrival_real_time.tzinfo) if arrival_real_time.tzinfo else datetime.now()
            arrival_real_diff = arrival_real_time - time_now

            arrival_seconds = int(arrival_real_diff.total_seconds())

            if arrival_seconds <= 0:
                arrival_in = f"{arrival_seconds} seconds"
            elif arrival_seconds < 60:
                arrival_in = f"{arrival_seconds} seconds"
            else:
                arrival_minutes = arrival_seconds // 60
                arrival_in = f"in {arrival_minutes} min"

            arrival_display = f"{arrival_real_time.astimezone().strftime('%H:%M')} ({arrival_in})"

        output_lines.append(f"{line_number:<8}{line_direction:<30}{arrival_display}")
    return "\n".join(output_lines)
    #except Exception as e:
    #    print("\aAn Error Occured")
    #    print(e)
    #return None


if __name__ == "__main__":
    userinput = input("Haltestelle: ")
    print(stop_info_tui(userinput))
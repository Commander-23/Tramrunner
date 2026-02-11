import utils, api
from datetime import datetime

def stop_info_tui(userinput:str=None):
    if userinput is not None:
        stopid = utils.get_stop_id_from_pointfinder(userinput)
    else:
        print("Please provide a stop name or ID.")
        return None
    
    #try:
    mode_of_transport =['Tram', 'CityBus', 'SuburbanRailway']
    departure_monitor_response = api.vvo_departure_monitor(stopid, limit=20, mot=mode_of_transport)
    station_name = departure_monitor_response['Name']
    station_city = departure_monitor_response['Place']
    expiration_time = utils.vvo_time_conv(departure_monitor_response['ExpirationTime'])
    expiration_time_human = expiration_time.strftime("%H:%M:%S")

    return_lines = []
    output_lines = [
        f"Abfahrten für '{station_name}':",
        f"{'nr':<5}{'Direction':<25}{'Time':<6}{'Diff'}",
        "-" * 48
    ]
    for departure in departure_monitor_response['Departures']:
        line_number = departure.get('LineName')
        line_direction = departure.get('Direction')[:24]

        arrival_scheduled_time = utils.vvo_time_conv(departure.get('ScheduledTime')).astimezone().strftime("%H:%M")
        
        arrival_display = arrival_scheduled_time

        if departure.get('RealTime'):
            arrival_real_time = utils.vvo_time_conv(departure.get('RealTime'))
            time_now = datetime.now(arrival_real_time.tzinfo) if arrival_real_time.tzinfo else datetime.now()
            arrival_real_diff = arrival_real_time - time_now

            arrival_seconds = int(arrival_real_diff.total_seconds())

            if arrival_seconds <= 0:
                arrival_in = f"{arrival_seconds} sec"
            elif arrival_seconds < 60:
                arrival_in = f"{arrival_seconds} sec"
            else:
                arrival_minutes = arrival_seconds // 60
                arrival_in = f"{arrival_minutes} min"

            arrival_display = f"{arrival_real_time.astimezone().strftime('%H:%M')} {arrival_in}"

        if departure.get('State') == 'Delayed':
            delay_display = "DLY"
        else: delay_display = ""
        return_lines.append(
            {
                "time_scheduled":arrival_scheduled_time,
                "time_relative":arrival_in,
                "nr":line_number,
                "direction":line_direction,
                "mot":"Tram"

            }
        )
        output_lines.append(f"{line_number:<5}{line_direction:<25}{arrival_display:<7}{delay_display:<5}")
    return return_lines#"\n".join(output_lines)
    #except Exception as e:
    #    print("\aAn Error Occured")
    #    print(e)
    #return None


if __name__ == "__main__":
    userinput = input("Haltestelle: ")
    for line in stop_info_tui(userinput):
        print(f"{line}")
    print("bye,bye")
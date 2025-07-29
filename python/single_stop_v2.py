#!/usr/bin/env python3

import dvb
import csv
import os

def get_stop_from_shortname(rawSearchInput, csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), '/home/cmdr/tramrunner/files/kuerzel_dresden.csv')
    searchTerm = rawSearchInput.upper()
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for line in csv_reader:
            if str(searchTerm) in line:
                return line[0]
    return None

def monitor_departures(rawSearchInput, time_offset=0, num_results=25, city='Dresden'):
    """
    Returns a formatted string of upcoming departures for a given stop.
    """
    if len(rawSearchInput) == 3:
        stop = get_stop_from_shortname(rawSearchInput)
    else:
        stop = rawSearchInput

    if not stop:
        return "Stop not found."

    out = dvb.monitor(stop, time_offset, num_results, city)
    output_lines = [f"\nAbfahrten für '{stop}':\n", f"{'Linie':<8}{'Richtung':<30}{'Ankunft':<10}", "-" * 48]
    for entry in out:
        line = entry.get('line', '')
        direction = entry.get('direction', '')
        arrival = entry.get('arrival', '')
        try:
            arrival_val = int(arrival)
        except (ValueError, TypeError):
            arrival_val = None
        if arrival_val is not None and arrival_val > 30:
            continue
        output_lines.append(f"{line:<8}{direction:<30}{arrival:<10}")
    return "\n".join(output_lines)

def print_departures(stop, departures):
    print(f"\nAbfahrten für '{stop}':")
    print(f"{'Linie':<8}{'Richtung':<30}{'Ankunft':<10}")
    print("-" * 48)
    for entry in departures:
        line = entry.get('line', '')
        direction = entry.get('direction', '')
        arrival = entry.get('arrival', '')
        print(f"{line:<8}{direction:<30}{arrival:<10}")

# Example usage:
if __name__ == "__main__":
    rawSearchInput = input('Haltestelle: ')
    print(monitor_departures(rawSearchInput))
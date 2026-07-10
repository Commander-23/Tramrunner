import csv
import os
from typing import Dict
import pprint


def web_get_json(url: str, nolines: bool) -> Dict:
    """
    Fetches data from the given URL and returns it as a JSON object.
    Args:
        url (str): URL to fetch the data from.
    Returns:
        dict: Parsed JSON data.
    """
    import requests
    
    if url is None:
        print("using default url")
        url = "https://www.vvo-online.de/open_data/vvo_stops.json"

    try:
        with requests.Session() as session:
            response = session.get(
                url,
                timeout=5,
                verify=True
            ) 
            response.raise_for_status()  # Raises an error for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    stations = response.json()

    
    geostations = []
    for station in stations:# Parse the JSON response
        if not nolines:
            for i in range(0, len(station['Lines']), 1):
                lines = station['Lines'][i]
        else:
            lines= []
        feature = {
            "type": "Feature",
            "properties": {
                "number": station['gid'],
                "id": station['id'],
                "nameWithCity": station['place']+' ' + station['name'],
                "name": station['name'],
                "city": station['place'],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(station['x'].replace(',', '.')) if station['x'] else 0.0,
                    float(station['y'].replace(',', '.')) if station['y'] else 0.0
                ] if station.get('x') and station.get('y') else [0.0, 0.0]
            },
            
            "Lines": lines
                
            }   
               
        geostations.append(feature)
    geojson = {
        "type": "FeatureCollection",
        "features": geostations
    }
    return geojson

def search_by_line_number(geojson: Dict, line_number: str) -> list:
    """
    Searches for features in a GeoJSON FeatureCollection that have a specific line number.
    Args:
        geojson (dict): GeoJSON FeatureCollection.
        line_number (str): The line number to search for.
    Returns:
        list: Features that have the specified line number.
    """
    matching_features = []
    for feature in geojson.get("features", []):
        lines = feature.get("Lines", [])
        if any(line.get("LineNr") == line_number for line in lines):
            matching_features.append(feature)
    return matching_features  # Return up to 5 matches


def format_out(data: Dict) -> str:
    """
    Returns a formatted string of upcoming departures for a given stop.
    """
    output_lines = []
    #output_lines = [f"\nAbfahrten für '{stop}':\n", f"{'Linie':<8}{'Richtung':<30}{'Ankunft':<10}", "-" * 48]
    for entry in data[2]:
        name = entry.get('nameWithCity', '')
        stop_id = entry.get('number', '')
        output_lines.append(f"{name:<8}{stop_id:<30}")
    return "\n".join(output_lines)
def print_results(results: list):
    #print(f"\nAbfahrten für '{stop}':")
    #print(f"{'Linie':<8}{'Richtung':<30}{'Ankunft':<10}")
    print(f"{'Name':<8}")
    print("-" * 48)
    for entry in results:
        name = entry.get('name', '')
        #direction = entry.get('direction', '')
        #arrival = entry.get('arrival', '')
        print(f"{name:<8}")



def print_output(data: Dict):
    """
    Prints the formatted output of the upcoming departures for a given stop.
    """
    
    print(f"\nAbfahrten für '{data[0]}':")
    print(f"{'Linie':<8}{'Richtung':<30}{'Ankunft':<10}")
    print("-" * 48)
    
    for entry in data[2]:
        name = entry.get('nameWithCity', '')
        stop_id = entry.get('number', '')
        print(f"{name:<8}{stop_id:<30}")


import csv
import json
import requests
from typing import Dict
import os
import pprint
import requests, json

def web_get_json(url: str) -> Dict:
    """
    Fetches data from the given URL and returns it as a JSON object.
    Args:
        url (str): URL to fetch the data from.
    Returns:
        dict: Parsed JSON data.
    """
    
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
        lines = station['Lines']
        feature = {
            "type": "Feature",
            "properties": {
                "number": station['gid'],
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
            "Lines": [station['Lines'][i] for i in range(0, len(station['Lines']), 1)]
                
            }   
               
        geostations.append(feature)
    geojson = {
        "type": "FeatureCollection",
        "features": geostations
    }
    return geojson
def csv_to_geojson(csv_path: str) -> Dict:
    """
    Converts a stations CSV file to a GeoJSON FeatureCollection.
    expectet CSV format:

    Args:
        csv_path (str): Path to the CSV file.
    Returns:
        dict: GeoJSON FeatureCollection.
    """

    # local_shortnames_csv_path = '/home/cmdr/dev-py/files/shortnames_dresden.csv'
    
    

    # local_source.csv
    # [['Nummer', 'Name mit Ort', 'Name ohne Ort', 'Ort', 'Tarifzone 1 ', 'Tarifzone 2', 'Tarifzone 3', 'WGS84_X', 'WGS84_Y'],
    # ['de:14612:1', 'Dresden Bahnhof Mitte', 'Bahnhof Mitte', 'Dresden', '0100', '', '', '13,723395', '51,055642'],

    stations = []
    with open(csv_path) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            stations.append(row)
    geostations = []
    for station in stations[1:]:
        feature = {
            "type": "Feature",
            "properties": {
                "number": station[0],
                "nameWithCity": station[1],
                "name": station[2],
                "city": station[3],
                "tariffZone1": station[4],
                "tariffZone2": station[5],
                "tariffZone3": station[6]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(station[7].replace(',', '.')),
                    float(station[8].replace(',', '.'))
                ]
            }
        }
        geostations.append(feature)
    geojson = {
        "type": "FeatureCollection",
        "features": geostations
    }
    return geojson
def write_to_json(json_data: Dict, output_path: str):
    """
    Writes a GeoJSON object to a file in JSON format.

        geojson (Dict): A dictionary representing a GeoJSON FeatureCollection.
        output_path (str): The file path where the GeoJSON will be saved.

    Raises:
        IOError: If the file cannot be written.
        TypeError: If the geojson object is not serializable.

    Example:
        write_to_json(feature_collection, '/path/to/output.json)
    """
    with open(output_path, mode='w', encoding='utf-8') as geojson_file:
        json.dump(json_data, geojson_file, ensure_ascii=False, indent=4)



def load_geojson(input_path: str) -> Dict:
    """
    Loads a GeoJSON file from the specified path.
    Args:
        input_path (str): Path to the GeoJSON file.
    Returns:
        dict: Loaded GeoJSON FeatureCollection.
    """
    with open(input_path, 'r') as geojson_file:
        return json.load(geojson_file)

def search_geojson(geojson: Dict, key: str, value: str):
    """
    Searches for features in a GeoJSON FeatureCollection by property key and value.
    Args:
        geojson (dict): GeoJSON FeatureCollection.
        key (str): Property key to search.
        value (str): Property value to match.
    Returns:
        list: Matching features.
    """
    return [
        feature for feature in geojson.get("features", [])
        if feature.get("properties", {}).get(key) == value
    ][:5]

def get_stop_from_shortname(rawSearchInput, csv_path=None):
    if csv_path is None:
        csv_path = os.path.join(os.path.dirname(__file__), 'shortnames_dresden.csv')
    searchTerm = rawSearchInput.upper()
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for line in csv_reader:
            if str(searchTerm) in line:
                return line[0]
    return None



    




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



if __name__ == "__main__":

    local_shortnames_csv_path = '/home/cmdr/dev-py/files/shortnames_dresden.csv'
    local_shortnames_json_path = '/home/cmdr/dev-py/files/shortnames_dresden.json'
    local_source_csv_path = '/home/cmdr/dev-py/files/local_source.csv'
    local_static_json_path = '/home/cmdr/dev-py/files/local_static.json'
    web_daily_url = "https://www.vvo-online.de/open_data/vvo_stops.json"
    web_daily_json_path = '/home/cmdr/dev-py/files/web_daily_json.json'
    
    print("\n"*2)

    # Convert CSV to GeoJSON and save it
    #write_to_json(csv_to_geojson(local_source_csv_path), local_static_json_path)
    #print(f"local copy saved to {local_static_json_path}")


    

    data = web_get_json(web_daily_url)
    if data is None:
        
        data = load_geojson(local_static_json_path)
        print(f"Loaded local static data from {local_static_json_path}")
    elif data is None:
        print(f"Failed to fetch data from {web_daily_url} and no local static data found.")
        exit(1)


    

    write_to_json(data, web_daily_json_path)
    print(f"local copy saved to {web_daily_json_path}")
    print(f"Number of features: {len(data['features'])}")


    print("\n"*3)
    search_key = 'city'
    search_value = 'Dresden'
    results = search_geojson(data, search_key, search_value)
    
    print("\nGeoJSON FeatureCollection (pretty print):")
    pprint.pprint(results, indent=2, width=120)
    
    # Access first 3 Lines entries for each result
    print("\nFirst 3 Lines for each result:")
    for feature in results:
        stop_name = feature['properties']['name']
        lines = feature['Lines'][:10]  # Get first 3 lines
        print(f"\nStop: {stop_name}")
        for line in lines:
            print(f"Line {line['LineNr']}: {line['Route']}")



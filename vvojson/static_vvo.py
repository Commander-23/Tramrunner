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
    
    








    #stations = []
    stations = response.json()
    # Convert each stop to a GeoJSON feature
    geostations = []
    for station in stations:# Parse the JSON response
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
            "Lines": station.get('Lines', []),  # Include Lines array, empty list if not present
            
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
    Args:
        csv_path (str): Path to the CSV file.
    Returns:
        dict: GeoJSON FeatureCollection.
    """
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


def write_geojson(geojson: Dict, output_path: str):
    """
    Writes a GeoJSON object to a file.
    Args:
        geojson (dict): GeoJSON FeatureCollection.
        output_path (str): Path to output file.
    """
    with open(output_path, mode='w', encoding='utf-8') as geojson_file:
        json.dump(geojson, geojson_file, ensure_ascii=False, indent=4)
      


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





if __name__ == "__main__":
    local_source_csv_path = '/home/cmdr/dev-py/stations/local_source.csv'
    local_static_json_path = '/home/cmdr/dev-py/stations/local_static.json'
    web_daily_url = "https://www.vvo-online.de/open_data/vvo_stops.json"
    web_daily_json_path = '/home/cmdr/dev-py/stations/web_daily_json.json'
    
    print("\n"*2)










    
    #search_key = 'nameWithCity'
    #search_value = 'Dresden Bahnhof Mitte'
    #results = search_geojson(geojson, search_key, search_value)
    #print(f"Found {len(results)} results for {search_key}='{search_value}':", results)
    write_geojson(csv_to_geojson(local_source_csv_path), local_static_json_path)


    data = web_get_json(web_daily_url)
    if data is None:
        
        data = load_geojson(local_static_json_path)
        print(f"Loaded local static data from {local_static_json_path}")
    elif data is None:
        print(f"Failed to fetch data from {web_daily_url} and no local static data found.")
        exit(1)


    

    write_geojson(data, web_daily_json_path)
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



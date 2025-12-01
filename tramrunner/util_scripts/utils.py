import pathlib
import requests
import json

base_dir = pathlib.Path(__file__).parent.parent.parent


def web_get(url:str):
    """
    simple web get
    """
    try:
        with requests.Session() as session:
            response = session.get(url)
            response.raise_for_status()
            return response
    except requests.exceptions.RequestException as e:
        print(f"Failed to access: {e}")
        return None

def update_static_files():
    """
    Update the static files in the project.
    source: https://github.com/kiliankoe/vvo

    there is a nice formating script in the scripts dir of this repo kiliankoe/vvo
    """
    static_file_dir = base_dir/'data'/'static_files'
    static_urls = {
        'stations.json':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/stations.json",
        'stations.geojson':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/stations.geojson",
        'stations.csv':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/stations.csv",
        'stations_summary.md':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/stations_summary.md",
        'abbreviations_dresden.csv':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/abbreviations_dresden.csv",
        'abbreviations_regional.csv':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/abbreviations_regional.csv",
        'vvo_stops.json':"https://www.vvo-online.de/open_data/VVO_STOPS.JSON"
    }

    for file_name, url in static_urls.items():
        print(f"Downloading {file_name} from {url}...")
        response = requests.get(url)
        if response is not None:
            with open(f"{static_file_dir}/{file_name}", "wb") as f:
                f.write(response.content)
                print(f"saved")

def write_to_json(json_data: dict, file_name: str):
    json_dir = base_dir/'data'/'generated_files'
    output_path = json_dir/file_name
    with open(output_path, mode='w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    some_json = {
        
        "Name": "Hauptbahnhof",
        "Status": {
            "Code": "Ok"
        },
        "Place": "Dresden"
    }

    write_to_json(some_json, "test_file.json")

import os
import requests


def update_static_files():
    """
    Update the static files in the project.
    source: https://github.com/kiliankoe/vvo
    """

    static_urls={
        'stations.json':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/stations.json",
        'stations.geojson':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/stations.geojson",
        'stations.csv':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/stations.csv",
        'stations_summary.md':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/stations_summary.md",
        'abbreviations_dresden.csv':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/abbreviations_dresden.csv",
        'abbreviations_regional.csv':"https://raw.githubusercontent.com/kiliankoe/vvo/master/data/abbreviations_regional.csv",
        'vvo_stops.json':"https://www.vvo-online.de/open_data/VVO_STOPS.JSON"
    }

    for file_name, url in static_urls.items():
        
        print(file_name)
        print(url)
        
        #try:
        #    with requests.Session() as session:
        #        response = session.get(static_url)
        #        response.raise_for_status()
        #except requests.RequestException as web_get_err:
        #    print(f"Error fetching data: {web_get_err}")
        #    return None


if __name__ == "__main__":
    update_static_files()

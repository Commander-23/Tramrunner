import requests
from static_vvo import write_to_json, web_get_json, load_geojson, search_geojson







def get_stop_info(query: str) -> dict:
    """
    Fetches information about a specific stop using its ID.
    
    Args:
        stop_id (str): The ID of the stop to fetch information for.
        
    Returns:
        dict: A dictionary containing stop information.
    """

    base_url = "https://webapi.vvo-online.de/tr/pointfinder"
    headers = {
    "Content-Type": "application/json",
    "charset": "utf-8"
    }
    params = {
        "query": query,
        "stopsOnly": True
    }

    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()  # Raise an error for bad responses
    if response.status_code == 200:
        return response.json()  # parse JSON response
    else:
        print(f"Request failed with status {response.status_code}: {response.text}")



if 1 == 1:
    #
    data = web_get_json(url=None,nolines=True)
    #print(data)
    search_key = 'name'
    search_value = 'Bahnhof Mitte'
    results = search_geojson(data, search_key, search_value)
    #print(results)
    print(results[0]['properties']['id'])

    api_result = get_stop_info(results[0]['properties']['id'])
    write_to_json(api_result, "/home/cmdr/dev-py/files/pointfinder.json")

    
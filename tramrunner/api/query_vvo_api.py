import json, requests

def query_vvo_api(url: str, headers: dict, params: dict = None) -> dict:
    """
    Query the VVO API to get information about stops, departures, and trips.
    """
    if not url:
        raise ValueError("URL cannot be empty.")
    if not headers:
        headers = {
            "Content-Type": "application/json",
            "charset": "utf-8"
        }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10, verify=True) 
        if response.status_code == 200:
            content = json.loads(response.content.decode('utf-8'))
            
            output = content #content['Points'][0].split('|')
            # outputs the first point in the list, e.g. ['33000313', '', 'Räcknitzhöhe', '5655709', '4622355', '0', '']
            return output
        else:
            raise requests.HTTPError('HTTP Status: {}'.format(response.status_code))    
    except requests.RequestException as e:
        print(f"Failed to access VVO pointfinder. Request Exception", e)
        response = None
    
    if response is None:
        return None
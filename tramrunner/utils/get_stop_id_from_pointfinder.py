from api import vvo_pointfinder
def get_stop_id_from_pointfinder(query: str) -> str:
    """
    query the VVO pointfinder API to get the stop ID for a given query.

    Args:
        query (str): The query to search for in the VVO API.

    Returns:
        str: The stop ID for the given query.
    """
    api_response = vvo_pointfinder(query=query, limit=10, stopsOnly=True, regionalOnly=True)
    if api_response is not None and 'Points' in api_response:
        return api_response['Points'][0].split('|')[0]
    else:
        print("Failed to retrieve stop ID from pointfinder.")
        return None

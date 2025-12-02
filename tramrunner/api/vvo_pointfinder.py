from api import query_vvo_api
def vvo_pointfinder(query: str, limit: int = 0, stopsOnly: bool = False, regionalOnly: bool = False, stopShortcuts: bool = False):
    """
    Find stops based certain parameters.
    """
   
    defaulturl = "https://webapi.vvo-online.de/tr/pointfinder"

    if not query:
        raise ValueError("Query parameter cannot be empty.")
    
    
    query_params = {
        "query": query,
        "limit": limit,
        "stopsOnly": stopsOnly,
        "regionalOnly": regionalOnly,
        "stopShortcuts": stopShortcuts
    }
    # {'query': 'Räcknitzhöhe', 'limit': 10, 'stopsOnly': True, 'regionalOnly': False, 'stopShortcuts': False}
    return query_vvo_api(defaulturl, None, query_params)
 
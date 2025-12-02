from api import query_vvo_api
def vvo_lines(stopid: str):
    """
    Get informatin about wich lines do service a stop.
    """
    defaulturl = "https://webapi.vvo-online.de/stt/lines"
    if not stopid:
        raise ValueError("Stop ID cannot be empty.")
    
    query_params = {"stopid": stopid}
    
    return query_vvo_api(defaulturl, None, query_params)

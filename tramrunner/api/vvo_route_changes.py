from api import query_vvo_api
def vvo_route_changes(shortterm: bool = True):
    """
    Get information about route changes because of construction work or such.
    Arguments:
        shortterm : unknown. I diffed the output with and without -> no diff
    """
    defaulturl = "https://webapi.vvo-online.de/rc"

    query_params = {"shortterm": shortterm}

    return query_vvo_api(defaulturl, None, query_params)

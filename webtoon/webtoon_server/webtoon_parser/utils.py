from urllib.parse import urlencode, urljoin


def append_query_to_url(base_url, params):
    """
    :param base_url:
    :param params: dict type
    :return: http://test?test=1&test2=2
    """
    query = urlencode(params)
    return base_url + '?' + query


def append_fragment_to_url(base_url, params):
    query = '#' + urlencode(params)
    return urljoin(base_url, query)

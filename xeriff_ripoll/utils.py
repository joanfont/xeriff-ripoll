from urllib.parse import urlparse, parse_qs

def get_querystring_from_url(url: str) -> dict:
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)

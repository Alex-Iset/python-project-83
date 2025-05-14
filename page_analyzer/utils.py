from urllib.parse import urlparse


def normalize_url(url):
    parse = urlparse(url)
    return f"{parse.scheme}://{parse.netloc}"

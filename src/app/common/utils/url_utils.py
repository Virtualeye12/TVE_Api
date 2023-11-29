from urllib.parse import urlparse
import furl


def url_normalization(url):
    """
    Url normalization rules
    1. stripAuthentication
    2. stripHash
    3. stripProtocol
    4. stripWWW
    5. removeQueryParameters
    6. removeTrailingSlash
    """

    "stripAuthentication"
    try:
        url = url.split("@")
        if len(url) > 1:
            url = url[1]
        else:
            url = url[0]
    except:
        url = url

    "stripHash"
    try:
        url = url.split("#")
        if len(url) > 1:
            url = url[1]
        else:
            url = url[0]
    except:
        url = url

    "stripProtocol"
    try:
        parsed = urlparse(url)
        scheme = "%s://" % parsed.scheme
        url = (parsed.geturl().replace(scheme, '', 1))
        if url.startswith('www.'):
            url = url[4:]
    except:
        url = url

    "stripWWW"
    try:
        if url.startswith('www.'):
            url = url[4:]
    except:
        url = url

    "removeQueryParameters"
    try:
        url = furl.furl(url).remove(args=True, fragment=True).url
    except:
        url = url

    "removeTrailingSlash"
    try:
        if url.endswith('/'):
            url = url[:-1]
    except:
        url = url

    return url

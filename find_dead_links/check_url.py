import time

import requests

HTTP_OK = 200


def check_url(url: str, website_domain: str, sleep_time: float = 0.1, timeout: int = 5) -> tuple[bool, str]:
    """Check if a URL is reachable (returns HTTP status code 200).

    If the URL is relative, it is resolved against the given website domain.

    Args:
        url (str): The URL to check.
        website_domain (str): The domain of the website being checked.
        sleep_time (float): The time to sleep between requests.
        timeout (int): The timeout for the request.

    Returns
    -------
        tuple[bool, str]: A tuple containing a boolean indicating if the URL is reachable
                          and a string with any error message.
    """
    if url.startswith("/"):
        url = website_domain.rstrip("/") + url
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        time.sleep(sleep_time)
    except requests.RequestException as e:
        return False, str(e)
    else:
        return response.status_code == HTTP_OK, ""

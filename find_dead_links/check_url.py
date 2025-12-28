import time

import requests
import urllib3

urllib3.disable_warnings()

HTTP_OK = 200
FORBIDDEN = 403
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
}


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
        if response.status_code == FORBIDDEN:
            response = requests.head(url, headers=HEADERS, allow_redirects=True, timeout=timeout, verify=False)  # noqa: S501
            time.sleep(sleep_time)
    except requests.RequestException as e:
        return False, str(e)
    else:
        return response.status_code == HTTP_OK, ""

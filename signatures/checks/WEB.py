from domain import Domain
from math import floor
import logging


def string_in_body(
    domain: Domain, string: str, https: bool, custom_uri: str = ""
) -> bool:
    if string in domain.fetch_web(https=https, uri=custom_uri).body:
        logging.info(f"Message observed in response for '{domain}'")
        return True
    logging.debug(f"Message not found in response for '{domain}'")
    return False


def string_in_body_http(domain: Domain, string: str, custom_uri: str = "") -> bool:
    return string_in_body(domain, string, False, custom_uri)


def string_in_body_https(domain: Domain, string: str, custom_uri: str = "") -> bool:
    return string_in_body(domain, string, True, custom_uri)


def status_code_match(domain: Domain, status_code: int, https: bool) -> bool:
    response_code = domain.fetch_web(https=https).status_code
    if status_code < 10:  # match the first int
        if floor(response_code / 100) == status_code:
            logging.info(f"Response code {response_code} observed for '{domain}'")
            return True
    else:
        if response_code == status_code:
            logging.info(f"Response code {response_code} observed for '{domain}'")
            return True
    logging.debug(f"Response code {response_code} observed for '{domain}'")
    return False


def status_code_404(domain: Domain, https: bool) -> bool:
    return status_code_match(domain, 404, https)

from domain import Domain
from . import helpers
import logging


def string_in_body(domain: Domain, string: str, https: bool) -> bool:
    if string in domain.fetch_web(https=https).body:
        logging.info(f"Message observed in response for '{domain}'")
        return True
    logging.debug(f"Message not found in response for '{domain}'")
    return False


def string_in_body_http(domain: Domain, string: str) -> bool:
    return string_in_body(domain, string, False)


def string_in_body_https(domain: Domain, string: str) -> bool:
    return string_in_body(domain, string, True)

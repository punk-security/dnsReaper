from domain import Domain
from . import helpers
import logging


def match(domain: Domain, strings) -> str:
    match = helpers.substrings_in_strings(strings, domain.CNAME)
    if match:
        logging.debug(f"Match detected in CNAME '{match} for domain '{domain}'")
        return True
    return False

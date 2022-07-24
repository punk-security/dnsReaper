from domain import Domain
from . import helpers
import logging


def match(domain: Domain, strings) -> str:
    match = helpers.substrings_in_strings(strings, domain.CNAME)
    if match:
        logging.debug(f"Match detected in CNAME '{match} for domain '{domain}'")
        return True
    return False


def NX_DOMAIN_on_resolve(domain: Domain) -> bool:
    for cname in domain.CNAME:
        cname = Domain(cname, fetch_standard_records=False)
        if cname.NX_DOMAIN:
            logging.info(f"NX_Domain for cname {cname}")
            return True
    return False

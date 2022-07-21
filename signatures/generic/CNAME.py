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
        cname = Domain(cname, fetch_standard_records=True)
        if cname.A != []:
            logging.debug(f"A records returned for cname {cname}")
            continue
        if cname.AAAA != []:
            logging.debug(f"AAAA records returned for cname {cname}")
            continue
        if cname.CNAME != []:
            logging.debug(f"NS records returned for cname {cname}")
            continue
        if cname.NS != []:
            logging.debug(f"NS records returned for cname {cname}")
            continue
        logging.debug(f"No records returned for domain {cname}")
        return True
    return False

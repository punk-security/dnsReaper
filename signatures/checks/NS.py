from domain import Domain
from . import helpers
import logging
import resolver as resolver


def match(domain: Domain, strings) -> str:
    match = helpers.substrings_in_strings(strings, domain.NS)
    if match:
        logging.debug(f"Match detected in NS '{match} for domain '{domain}'")
        return True
    return False


async def no_SOA_detected(domain: Domain) -> bool:
    for ns in domain.NS:
        ns_ip = await Domain(ns, fetch_standard_records=False).query("A")
        if ns_ip == []:
            logging.debug(f"Could not resolve NS '{ns}'")
            continue
        if (
            (await resolver.Resolver.resolve_with_ns(domain.domain, ns_ip[0], "SOA"))[
                "SOA"
            ]
        ) == []:
            logging.info(f"NAMESERVER at {ns} does not have this zone.")
            return True
        else:
            logging.debug(f"SOA record found on NAMESERVER '{ns}'")
    return False  # Never found the condition

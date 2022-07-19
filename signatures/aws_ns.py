from domain import Domain
import generic_checks
import logging

matching_ns_substring = "awsdns"


def potential(domain: Domain, **kwargs) -> bool:
    return generic_checks.string_in_ns(domain, matching_ns_substring)


def check(domain: Domain, **kwargs) -> bool:
    takeover_possible = False
    for ns in domain.NS:
        ns_ip = Domain(ns, fetch_standard_records=False).query("A")
        if ns_ip == []:
            logging.debug(f"Could not resolve NS '{ns}'")
            continue
        if Domain(domain.domain, fetch_standard_records=False, ns=ns_ip[0]).SOA == []:
            logging.info(f"NAMESERVER at {ns} does not have this zone.")
            takeover_possible = True
        else:
            logging.debug(f"SOA record found on NAMESERVER '{ns}'")
    return takeover_possible


INFO = """
The defined domain has NS records configured but these nameservers do not host a zone for this domain. \
An attacker can register this domain on AWS multiple times until they get provisioned onto a matching nameserver.
    """

from domain import Domain
import generic_checks

import logging

wordpress_ns = ["ns1.wordpress.com", "ns2.wordpress.com", "ns3.wordpress.com"]


def potential(domain: Domain, **kwargs) -> bool:
    return generic_checks.string_in_ns(domain, wordpress_ns)


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
The defined domain has NS records configured for wordpress.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """

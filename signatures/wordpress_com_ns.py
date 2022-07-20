from domain import Domain
import generic_checks

import logging

wordpress_ns = ["ns1.wordpress.com", "ns2.wordpress.com", "ns3.wordpress.com"]


def potential(domain: Domain, **kwargs) -> bool:
    return generic_checks.string_in_ns(domain, wordpress_ns)


def check(domain: Domain, **kwargs) -> bool:
    return generic_checks.no_SOA_on_NS(domain)


INFO = """
The defined domain has NS records configured for wordpress.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """

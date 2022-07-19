from domain import Domain
import generic_checks

import logging

wordpress_cname = "wordpress.com"
wordpress_ns = ["ns1.wordpress.com", "ns2.wordpress.com", "ns3.wordpress.com"]


def potential(domain: Domain, **kwargs) -> bool:
    if generic_checks.string_in_cname(domain, wordpress_cname):
        return True
    return generic_checks.string_in_ns(domain, wordpress_ns)


domain_not_configured_message = (
    "If this is your domain name and it has recently stopped working"
)


def check(domain: Domain, **kwargs) -> bool:
    return generic_checks.string_in_body(domain, domain_not_configured_message)


INFO = """
The defined domain has CNAME/NS records configured for wordpress.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """

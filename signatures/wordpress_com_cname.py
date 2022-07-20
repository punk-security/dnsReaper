from domain import Domain
import generic_checks

import logging

wordpress_cname = "wordpress.com"


def potential(domain: Domain, **kwargs) -> bool:
    return generic_checks.string_in_cname(domain, wordpress_cname)


domain_not_configured_message = (
    "If this is your domain name and it has recently stopped working"
)


def check(domain: Domain, **kwargs) -> bool:
    return generic_checks.string_in_body_https(domain, domain_not_configured_message)


INFO = """
The defined domain has CNAME records configured for wordpress.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """

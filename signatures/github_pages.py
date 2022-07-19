from domain import Domain

import generic_checks
import combined_checks


github_pages_ipv4 = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
]
github_pages_ipv6 = [
    "2606:50c0:8000::153",
    "2606:50c0:8001::153",
    "2606:50c0:8002::153",
    "2606:50c0:8003::153",
]


def potential(domain: Domain, **kwargs) -> bool:
    return combined_checks.matching_ipv4_or_ipv6(
        domain, github_pages_ipv4, github_pages_ipv6
    )


domain_not_configured_message = "There isn't a GitHub Pages site here"


def check(domain: Domain, **kwargs) -> bool:
    return generic_checks.string_in_body(domain, domain_not_configured_message)


INFO = """
The defined domain has A/AAAA records configured for Github pages but Github pages returns a 404. \
An attacker can register this domain on Github pages.
    """

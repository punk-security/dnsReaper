from domain import Domain

import logging

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
    for ipv4 in github_pages_ipv4:
        if ipv4 in domain.A:
            return True
    for ipv6 in github_pages_ipv6:
        if ipv6 in domain.AAAA:
            return True
    return False


def check(domain: Domain, **kwargs) -> bool:
    if domain.fetch_web().status_code == 404:
        return True
    return False


INFO = """
The defined domain has A/AAAA records configured for Github pages but Github pages returns a 404. \
An attacker can register this domain on Github pages.
    """

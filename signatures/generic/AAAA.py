from domain import Domain
import logging


def match(domain: Domain, ipv6) -> str:
    if type(ipv6) == str:
        ipv6 = [ipv6]
    for address in ipv6:
        if address in domain.AAAA:
            logging.debug(f"IPv6 address detected for domain '{domain}'")
            return True
    return False

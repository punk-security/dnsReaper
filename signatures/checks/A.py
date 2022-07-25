from domain import Domain
import logging


def match(domain: Domain, ipv4) -> str:
    if type(ipv4) == str:
        ipv4 = [ipv4]
    for address in ipv4:
        if address in domain.A:
            logging.debug(f"IPv4 address '{address}' detected for domain '{domain}'")
            return True
    return False

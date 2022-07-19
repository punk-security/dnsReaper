from domain import Domain
import logging


def string_in_body(domain: Domain, string: str) -> bool:
    if string in domain.fetch_web().body:
        logging.info(f"Message not observed in response for '{domain}'")
        return True
    logging.debug(f"Message found in reponse for '{domain}'")
    return False


def substrings_in_strings(substrings, strings):
    if type(strings) != list:
        strings = [strings]
    if type(substrings) != list:
        substrings = [substrings]
    for string in strings:
        for substring in substrings:
            if substring == "":
                continue
            if substring in string:
                return string
    return ""


def string_in_cname(domain: Domain, strings) -> str:
    match = substrings_in_strings(strings, domain.CNAME)
    if match:
        logging.debug(f"Match detected in CNAME '{match} for domain '{domain}'")
        return True
    return False


def string_in_ns(domain: Domain, strings) -> str:
    match = substrings_in_strings(strings, domain.NS)
    if match:
        logging.debug(f"Match detected in NS '{match} for domain '{domain}'")
        return True
    return False


def ipv4_in_A(domain: Domain, ipv4) -> str:
    if type(ipv4) == str:
        ipv4 = [ipv4]
    for address in ipv4:
        if address in domain.A:
            logging.debug(f"IPv4 address '{address}' detected for domain '{domain}'")
            return True
    return False


def ipv6_in_AAAA(domain: Domain, ipv6) -> str:
    if type(ipv6) == str:
        ipv6 = [ipv6]
    for address in ipv6:
        if address in domain.AAAA:
            logging.debug(f"IPv6 address detected for domain '{domain}'")
            return True
    return False

from domain import Domain
import logging


def string_in_body(domain: Domain, string: str, https: bool) -> bool:
    if string in domain.fetch_web(https=https).body:
        logging.info(f"Message observed in response for '{domain}'")
        return True
    logging.debug(f"Message not found in response for '{domain}'")
    return False


def string_in_body_http(domain: Domain, string: str) -> bool:
    return string_in_body(domain, string, False)


def string_in_body_https(domain: Domain, string: str) -> bool:
    return string_in_body(domain, string, True)


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


def no_SOA_on_NS(domain: Domain) -> bool:
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

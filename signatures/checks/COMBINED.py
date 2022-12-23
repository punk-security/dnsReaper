from . import A, AAAA, CNAME
from domain import Domain


def matching_ipv4_or_ipv6(domain: Domain, ipv4, ipv6) -> bool:
    if A.match(domain, ipv4):
        return True
    if AAAA.match(domain, ipv6):
        return True
    return False


def matching_ipv4_or_cname(domain: Domain, ipv4, strings) -> bool:
    if A.match(domain, ipv4):
        return True
    if CNAME.match(domain, strings):
        return True
    return False


def matching_ip_or_cname(domain: Domain, strings, ips) -> bool:
    if A.match(domain, ips):
        return True
    if AAAA.match(domain, ips):
        return True
    if CNAME.match(domain, strings):
        return True
    return False

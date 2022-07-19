from domain import Domain
import generic_checks


def matching_ipv4_or_ipv6(domain: Domain, ipv4, ipv6) -> bool:
    if generic_checks.ipv4_in_A(domain, ipv4):
        return True
    if generic_checks.ipv6_in_AAAA(domain, ipv6):
        return True
    return False


def matching_ipv4_or_cname(domain: Domain, ipv4, strings) -> bool:
    if generic_checks.ipv4_in_A(domain, ipv4):
        return True
    if generic_checks.string_in_cname(domain, strings):
        return True
    return False

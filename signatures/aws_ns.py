from domain import Domain
import generic_checks
import logging

matching_ns_substring = "awsdns"


def potential(domain: Domain, **kwargs) -> bool:
    return generic_checks.string_in_ns(domain, matching_ns_substring)


def check(domain: Domain, **kwargs) -> bool:
    return generic_checks.no_SOA_on_NS(domain)


INFO = """
The defined domain has NS records configured but these nameservers do not host a zone for this domain. \
An attacker can register this domain on AWS multiple times until they get provisioned onto a matching nameserver.
    """

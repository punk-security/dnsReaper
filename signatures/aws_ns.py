from domain import Domain
from . import generic

matching_ns_substring = "awsdns"


def potential(domain: Domain, **kwargs) -> bool:
    return generic.NS.match(domain, matching_ns_substring)


def check(domain: Domain, **kwargs) -> bool:
    return generic.NS.no_SOA_detected(domain)


INFO = """
The defined domain has NS records configured but these nameservers do not host a zone for this domain. \
An attacker can register this domain on AWS multiple times until they get provisioned onto a matching nameserver.
    """

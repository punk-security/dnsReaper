from domain import Domain
from . import generic

wordpress_ns = ["ns1.wordpress.com", "ns2.wordpress.com", "ns3.wordpress.com"]


def potential(domain: Domain, **kwargs) -> bool:
    return generic.NS.match(domain, wordpress_ns)


def check(domain: Domain, **kwargs) -> bool:
    return generic.NS.no_SOA(domain)


INFO = """
The defined domain has NS records configured for wordpress.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """

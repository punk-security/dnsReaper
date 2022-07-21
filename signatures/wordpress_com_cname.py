from domain import Domain
from . import generic

wordpress_cname = "wordpress.com"


def potential(domain: Domain, **kwargs) -> bool:
    return generic.CNAME.match(domain, wordpress_cname)


domain_not_configured_message = (
    "If this is your domain name and it has recently stopped working"
)


def check(domain: Domain, **kwargs) -> bool:
    return generic.WEB.string_in_body_https(domain, domain_not_configured_message)


INFO = """
The defined domain has CNAME records configured for wordpress.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """

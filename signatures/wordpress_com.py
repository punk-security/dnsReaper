from domain import Domain

import logging

wordpress_cname = "wordpress.com"
wordpress_ns = ["ns1.wordpress.com", "ns2.wordpress.com", "ns3.wordpress.com"]
wordpress_missconfigured_message = (
    "If this is your domain name and it has recently stopped working"
)


def potential(domain: Domain, **kwargs) -> bool:
    for cname in domain.CNAME:
        if wordpress_cname in cname:
            logging.debug(f"Wordpress CNAME detected for domain '{domain}'")
            return True

    for nameserver in domain.NS:
        if nameserver in wordpress_ns:
            logging.debug(f"Wordpress NS record found '{nameserver}'")
            return True
    return False


def check(domain: Domain, **kwargs) -> bool:
    if wordpress_missconfigured_message in domain.fetch_web().body:
        logging.info(f"Wordpress not configured for domain '{domain}'")
        return True
    logging.debug(f"wordpress 'not configured' page NOT found on the domain '{domain}'")
    return False


INFO = """
The defined domain has CNAME/NS records configured for wordpress.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """

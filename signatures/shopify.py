from domain import Domain

import logging

shopify_ipv4 = "23.227.38.65"
shopify_cname = "shops.myshopify.com"
domain_not_configured_message = "Only one step left!"


def potential(domain: Domain, **kwargs) -> bool:
    if shopify_ipv4 in domain.A:
        logging.debug(f"Shopify IPv4 address detected for domain '{domain}'")
        return True
    if shopify_cname in domain.CNAME:
        logging.debug(f"Shopify CNAME detected for domain '{domain}'")
        return True
    return False


def check(domain: Domain, **kwargs) -> bool:
    if domain_not_configured_message in domain.fetch_web().body:
        logging.info(f"Shopify not configured for domain '{domain}'")
        return True
    logging.debug(f"Shopify 'not configured' page NOT found on the domain '{domain}'")
    return False


INFO = """
The defined domain has A/CNAME records configured for Shopify pages but Shopify lets us know its not claimed. \
An attacker can register this domain on Shopify pages.

    """

# https://help.shopify.com/en/manual/domains/add-a-domain/connecting-domains/connect-domain-manual#step-1-change-your-dns-records-in-your-third-party-domain-provider-account

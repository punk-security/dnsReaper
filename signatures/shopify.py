from domain import Domain
from . import generic
import detection_enums

shopify_ipv4 = "23.227.38.65"
shopify_cname = "shops.myshopify.com"


def potential(domain: Domain, **kwargs) -> bool:
    return generic.COMBINED.matching_ipv4_or_cname(domain, shopify_ipv4, shopify_cname)


domain_not_configured_message = "Only one step left!"


def check(domain: Domain, **kwargs) -> bool:
    return generic.WEB.string_in_body_http(domain, domain_not_configured_message)


INFO = """
The defined domain has A/CNAME records configured for Shopify pages but Shopify lets us know its not claimed. \
An attacker can register this domain on Shopify pages.

    """

CONFIDENCE = detection_enums.CONFIDENCE.CONFIRMED

# https://help.shopify.com/en/manual/domains/add-a-domain/connecting-domains/connect-domain-manual#step-1-change-your-dns-records-in-your-third-party-domain-provider-account

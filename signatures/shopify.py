from .templates.cname_or_ip_found_but_string_in_body import (
    cname_or_ip_found_but_string_in_body,
)

ipv4 = ["23.227.38.65"]
ipv6 = []

cname = "shops.myshopify.com"

test = cname_or_ip_found_but_string_in_body(
    cname=cname,
    ips=ipv4 + ipv6,
    domain_not_configured_message="This domain points to Shopify but isn't configured properly",
    service="Shopify",
)

# https://help.shopify.com/en/manual/domains/add-a-domain/connecting-domains/connect-domain-manual#step-1-change-your-dns-records-in-your-third-party-domain-provider-account

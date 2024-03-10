from .templates.cname_or_ip_found_but_string_in_body import (
    cname_or_ip_found_but_string_in_body,
)

github_pages_ipv4 = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
]
github_pages_ipv6 = [
    "2606:50c0:8000::153",
    "2606:50c0:8001::153",
    "2606:50c0:8002::153",
    "2606:50c0:8003::153",
]

github_pages_cname = ".github.io"

test = cname_or_ip_found_but_string_in_body(
    cname=github_pages_cname,
    ips=github_pages_ipv4 + github_pages_ipv6,
    domain_not_configured_message="<title>Site not found ",
    service="Github Pages",
    https=True,
)

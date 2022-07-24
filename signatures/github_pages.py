from .templates.ip_found_but_string_in_body import ip_found_but_string_in_body

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

test = ip_found_but_string_in_body(
    ips=github_pages_ipv4 + github_pages_ipv6,
    domain_not_configured_message="There isn't a GitHub Pages site here",
    service="Github Pages",
)

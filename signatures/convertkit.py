from .templates.ip_found_but_string_in_body import ip_found_but_string_in_body

convertkit_pages_ipv4 = [
    "3.13.222.255",
    "3.13.246.91",
    "3.130.60.26",
]

test = ip_found_but_string_in_body(
    ips=convertkit_pages_ipv4,
    domain_not_configured_message="The page you were looking for doesn",
    service="Convert Pages",
)

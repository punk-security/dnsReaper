from .templates.ip_found_but_string_in_body import ip_found_but_string_in_body

test = ip_found_but_string_in_body(
    ips=["52.16.160.97"],
    domain_not_configured_message="job board website is either expired or its domain name is invalid.",
    service="smartjobboard.com",
    https=True,
)

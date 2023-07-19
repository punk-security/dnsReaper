from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".bigcartel.com",
    domain_not_configured_message="DNS resolution error",
    service="bigcartel.com",
)

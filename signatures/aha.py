from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".aha.io",
    domain_not_configured_message="invalid-portal",
    service="aha.io",
)

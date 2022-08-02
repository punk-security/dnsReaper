from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.aha.io",
    domain_not_configured_message="Unable to load ideas portal",
    service="aha.io",
)

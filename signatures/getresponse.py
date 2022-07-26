from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".gr8.com",
    domain_not_configured_message="is no longer available",
    service="getresponse",
)

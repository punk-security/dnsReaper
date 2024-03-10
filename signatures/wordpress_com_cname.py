from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".wordpress.com",
    domain_not_configured_message="Do you want to register",
    service="wordpress.com",
    https=True,
)

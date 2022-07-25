from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.wishpond.com",
    domain_not_configured_message="404",
    service="wishpond.com",
)

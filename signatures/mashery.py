from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".mashery.com",
    domain_not_configured_message="Unrecognized domain",
    service="mashery.com",
    https=True,
)

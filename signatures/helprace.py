from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".helprace.com",
    domain_not_configured_message="There is no account configured for this address!",
    service="helprace.com",
    https=True,
)

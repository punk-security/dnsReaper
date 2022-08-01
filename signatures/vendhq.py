from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.vendhq.com",
    domain_not_configured_message="Sign in to Lightspeed Retail POS Software | Lightspeed Retail",
    service="vendhq.com",
    https=True,
)

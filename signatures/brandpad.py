from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="brandpad.io",
    domain_not_configured_message="is not registered as whitelabel or custom domain.",
    service="brandpad.io",
)

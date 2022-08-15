from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.short.io",
    domain_not_configured_message="This domain is not configured on Short.io.",
    service="short",
    https=True,
)

from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".hatenablog.com",
    domain_not_configured_message="The request could not be satisfied.",
    service="hatenablog.com",
    https=False,
)

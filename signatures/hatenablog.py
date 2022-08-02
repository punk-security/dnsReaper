from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".hatenablog.com",
    domain_not_configured_message="404 Blog is not found",
    service="hatenablog.com",
    https=True,
)

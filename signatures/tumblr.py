from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".tumblr.com",
    domain_not_configured_message="There's nothing here.",
    service="tumblr.com",
)

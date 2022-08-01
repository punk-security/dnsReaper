from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".thinkific.com",
    domain_not_configured_message="The page you were looking for doesn't exist.",
    service="thinkific.com",
)

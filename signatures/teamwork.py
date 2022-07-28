from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".teamwork.com",
    domain_not_configured_message="Oops - We didn't find your site.",
    service="teamwork",
)

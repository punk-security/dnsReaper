from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.helpscoutdocs.com",
    domain_not_configured_message="Not Found",
    service="helpscoutdocs.com",
    https=True,
)

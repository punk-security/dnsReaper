from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.simplebooklet.com",
    domain_not_configured_message="you're looking for isn't here.",
    service="simplebooklet.com",
    https=True,
)

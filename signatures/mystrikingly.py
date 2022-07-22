from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.mystrikingly.com",
    domain_not_configured_message="Invalid URL",
    service="strikingly.com",
)

from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="wordpress.com",
    domain_not_configured_message="If this is your domain name and it has recently stopped working",
    service="wordpress.com",
)

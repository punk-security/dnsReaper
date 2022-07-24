from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.mysmartjobboard.com",
    domain_not_configured_message="Job Board Is Unavailable",
    service="mysmartjobboard.com",
    https=True,
)

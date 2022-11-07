from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".surveysparrow.com",
    domain_not_configured_message="<h5>Account not found.</h5>",
    service="survey sparrow",
)

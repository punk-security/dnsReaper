from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".surveysparrow.com",
    domain_not_configured_message="<title>DNS resolution error ",
    service="survey sparrow",
)

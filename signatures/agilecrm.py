from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.agilecrm.com",
    domain_not_configured_message="No landing page found.",
    service="agilecrm.com",
)

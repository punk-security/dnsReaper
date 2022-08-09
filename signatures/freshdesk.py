from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".freshdesk.com",
    domain_not_configured_message="no-helpdesk",
    service="freshdesk.com",
)

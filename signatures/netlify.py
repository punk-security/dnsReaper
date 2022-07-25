from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".netlify.app",
    domain_not_configured_message="Not Found - Request ID:",
    service="Netlify",
)

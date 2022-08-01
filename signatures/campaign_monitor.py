from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="goose.campaignmonitor.com",
    domain_not_configured_message="WHOOPS! The page you're looking for does not exist.",
    service="campaignmonitor.com",
)

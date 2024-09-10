from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="host.launchrock.com",
    domain_not_configured_message="It looks like you may have taken a wrong turn somewhere",
    service="Launchrock",
    https=True,
)

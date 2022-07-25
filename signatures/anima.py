from .templates.ip_found_but_string_in_body import ip_found_but_string_in_body

test = ip_found_but_string_in_body(
    ips="35.164.217.247",
    domain_not_configured_message="If this is your website and you’ve just created it, try refreshing in a minute",
    service="anima",
)

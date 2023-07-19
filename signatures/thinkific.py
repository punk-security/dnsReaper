from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".thinkific.com",
    domain_not_configured_message="Cloudflare is currently unable to resolve your requested domain",
    service="thinkific.com",
)

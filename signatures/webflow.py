from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=["cname.proxy.webflow.com", "cname.proxy-ssl.webflow.com"],
    domain_not_configured_message="404 - Page not found",
    service="webflow.com",
)

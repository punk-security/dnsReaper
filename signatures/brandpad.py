from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.brandpad.io",
    domain_not_configured_message="that doesnt match any whitelabels or custom-domains.",
    service="brandpad.io",
)

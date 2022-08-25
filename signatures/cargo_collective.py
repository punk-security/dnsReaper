from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.cargo.site",
    domain_not_configured_message="Should you require further assistance, please",
    service="Cargo Collective",
)

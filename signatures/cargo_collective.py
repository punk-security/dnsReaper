from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.cargo.site",
    domain_not_configured_message="404 Not Found",
    service="Cargo Collective",
)

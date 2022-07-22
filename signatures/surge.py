from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.surge.sh",
    domain_not_configured_message="project not found",
    service="surge.sh",
)

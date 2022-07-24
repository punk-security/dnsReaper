from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cname.myjetbrains.com",
    domain_not_configured_message="YouTrack Starting Page",
    service="myjetbrains.com",
)

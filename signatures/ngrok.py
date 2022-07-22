from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=[
        "cname.us.ngrok.io",
        "cname.eu.ngrok.io",
        "cname.uk.ngrok.io",
        "abc.cname.us.ngrok.io",
        "cname.ngrok.io",
    ],
    domain_not_configured_message="ERR_NGROK_3200",
    service="ngrok.io",
)

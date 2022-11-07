from .templates.ip_found_but_string_in_body import ip_found_but_string_in_body

test = ip_found_but_string_in_body(
    ips="35.164.217.247",
    domain_not_configured_message="""<h1>404 Not Found</h1></center>\r\n<hr><center>nginx</center>""",
    service="anima app",
)

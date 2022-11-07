from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="ns1.animaapp.com",
    domain_not_configured_message="""<h1>404 Not Found</h1></center>\r\n<hr><center>nginx</center>""",
    service="anima app",
)

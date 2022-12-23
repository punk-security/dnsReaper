from .templates.cname_or_ip_found_but_string_in_body import (
    cname_or_ip_found_but_string_in_body,
)

ipv4 = ["35.164.217.247"]
ipv6 = []

cname = "ns1.animaapp.com"

test = cname_or_ip_found_but_string_in_body(
    cname=cname,
    ips=ipv4 + ipv6,
    domain_not_configured_message="""<h1>404 Not Found</h1></center>\r\n<hr><center>nginx</center>""",
    service="anima app",
)

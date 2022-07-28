from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    ["ns1.domaindiscover.com", "ns2.domaindiscover.com"],
    service="tierra.net",
)

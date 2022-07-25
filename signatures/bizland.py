from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.bizland.com",
        "ns2.bizland.com",
        "clickme.click2site.com",
        "clickme2.click2site.com",
    ],
    service="bizland.com",
)

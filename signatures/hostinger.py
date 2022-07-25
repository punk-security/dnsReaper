from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.hostinger.com",
        "ns2.hostinger.com",
    ],
    service="hostinger.com",
)

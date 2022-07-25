from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.mediatemple.net",
        "ns2.mediatemple.net",
    ],
    service="mediatemple.net",
)

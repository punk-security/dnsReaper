from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.domain.com",
        "ns2.domain.com",
    ],
    service="domain.com",
)

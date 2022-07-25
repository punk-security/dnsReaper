from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.000domains.com",
        "ns2.000domains.com",
        "fwns1.000domains.com",
        "fwns2.000domains.com",
    ],
    service="000domains.com",
)

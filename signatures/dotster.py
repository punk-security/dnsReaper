from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.dotster.com",
        "ns2.dotster.com",
        "ns1.nameresolve.com",
        "ns2.nameresolve.com",
    ],
    service=[
        "nameresolve.com",
        "dotster.com",
    ],
)

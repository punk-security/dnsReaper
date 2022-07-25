from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "yns1.yahoo.com",
        "yns2.yahoo.com",
    ],
    service="yahoo.com",
)

from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.reg.ru",
        "ns2.reg.ru",
    ],
    service="reg.ru",
)

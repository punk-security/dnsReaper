from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns5.he.net",
        "ns4.he.net",
        "ns3.he.net",
        "ns2.he.net",
        "ns1.he.net",
    ],
    service="he.net",
)

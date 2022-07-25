from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.dnsimple.com",
        "ns2.dnsimple.com",
        "ns3.dnsimple.com",
        "ns4.dnsimple.com",
    ],
    service="dnsimple.com",
)

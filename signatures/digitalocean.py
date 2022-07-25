from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.digitalocean.com",
        "ns2.digitalocean.com",
        "ns3.digitalocean.com",
    ],
    service="digitalocean.com",
)

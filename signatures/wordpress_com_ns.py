from .routine.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    ["ns1.wordpress.com", "ns2.wordpress.com", "ns3.wordpress.com"],
    service="wordpress.com",
)

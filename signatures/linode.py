from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    [
        "ns1.linode.com",
        "ns2.linode.com",
    ],
    service="linode.com",
)

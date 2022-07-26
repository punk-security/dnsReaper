from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    ns=".nsone.net", service="ns1.com", sample_ns="dns1.p05.nsone.net"
)

from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    ns=".name.com", service="name.com", sample_ns="ns3nrz.name.com"
)

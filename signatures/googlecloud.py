from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    ns="googledomains",
    service="cloud.google.com",
    sample_ns="ns-cloud-b1.googledomains.com",
)

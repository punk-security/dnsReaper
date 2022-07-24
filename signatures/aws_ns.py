from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    ns="awsdns", service="AWS Route53", sample_ns="ns-40.awsdns-05.com"
)

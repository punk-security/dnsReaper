from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    ns="awsdns", service="AWS Route53", sample_ns="ns-40.awsdns-05.com"
)

test.INFO = (
    test.INFO
    + "  AWS has some validation that may prevent some takeovers, so this may or may not be vulnerable."
)

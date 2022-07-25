from .templates.ns_found_but_no_SOA import ns_found_but_no_SOA

test = ns_found_but_no_SOA(
    ns="dnsmadeeasy", service="dnsmadeeasy.com", sample_ns="ns11.dnsmadeeasy.com"
)

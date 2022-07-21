from .routine.ns_found_but_no_SOA import ns_found_but_no_SOA

INFO = """
The defined domain has NS records configured for wordpress.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """
test = ns_found_but_no_SOA(
    ["ns1.wordpress.com", "ns2.wordpress.com", "ns3.wordpress.com"], INFO
)

check = test.check
potential = test.potential
CONFIDENCE = test.CONFIDENCE
INFO = test.INFO

from .routine.ns_found_but_no_SOA import ns_found_but_no_SOA

INFO = """
The defined domain has NS records configured but these nameservers do not host a zone for this domain. \
An attacker can register this domain on AWS multiple times until they get provisioned onto a matching nameserver.
    """
test = ns_found_but_no_SOA("awsdns", INFO)

check = test.check
potential = test.potential
CONFIDENCE = test.CONFIDENCE
INFO = test.INFO

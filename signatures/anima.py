from .routine.ip_found_but_string_in_body import ip_found_but_string_in_body

INFO = """
The defined domain has CNAME records configured for Anima and is not claimed. \
An attacker can register this domain on Anima.

    """

test = ip_found_but_string_in_body(
    ips="35.164.217.247",
    domain_not_configured_message="If this is your website and you’ve just created it, try refreshing in a minute",
    info=INFO,
)

check = test.check
potential = test.potential
CONFIDENCE = test.CONFIDENCE
INFO = test.INFO

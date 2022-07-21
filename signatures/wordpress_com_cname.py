from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

INFO = """
The defined domain has CNAME records configured for wordpress.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """

test = cname_found_but_string_in_body(
    cname="wordpress.com",
    domain_not_configured_message="If this is your domain name and it has recently stopped working",
    info=INFO,
)

check = test.check
potential = test.potential
CONFIDENCE = test.CONFIDENCE
INFO = test.INFO

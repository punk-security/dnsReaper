from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

INFO = """
The defined domain has CNAME records configured for agilecrm.com and is not claimed. \
An attacker can register this domain on wordpress.com.

    """

test = cname_found_but_string_in_body(
    cname="cname.agilecrm.com",
    domain_not_configured_message="No landing page found.",
    info=INFO,
)

check = test.check
potential = test.potential
CONFIDENCE = test.CONFIDENCE
INFO = test.INFO

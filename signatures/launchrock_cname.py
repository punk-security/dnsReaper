from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

INFO = """
The defined domain has CNAME records configured for launchrock.com and is not claimed. \
An attacker can register this domain on launchrock.com

    """

test = cname_found_but_string_in_body(
    cname="cname.launchrock.com",
    domain_not_configured_message="It looks like you may have taken a wrong turn somewhere.",
    info=INFO,
    https=True
)

check = test.check
potential = test.potential
CONFIDENCE = test.CONFIDENCE
INFO = test.INFO


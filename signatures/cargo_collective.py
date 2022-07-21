from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

INFO = """
The defined domain has CNAME records configured for cargo.site and is not claimed. \
An attacker can register this domain on cargo.site.

    """

test = cname_found_but_string_in_body(
    cname="cname.cargo.site",
    domain_not_configured_message="404 Not Found",
    info=INFO,
)

check = test.check
potential = test.potential
CONFIDENCE = test.CONFIDENCE
INFO = test.INFO

from detection_enums import CONFIDENCE
from .templates.ip_found_but_string_in_body import ip_found_but_string_in_body


test = ip_found_but_string_in_body(
    ips=["23.236.62.147"],
    domain_not_configured_message="ConnectYourDomain",
    service="Wix",
)

test.CONFIDENCE = CONFIDENCE.POTENTIAL

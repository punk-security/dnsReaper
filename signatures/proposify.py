from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body
from detection_enums import CONFIDENCE

test = cname_found_but_string_in_body(
    cname="ssl.proposify.com",
    domain_not_configured_message="Why isn't my custom domain showing?",
    service="app.proposify.com",
    confidence=CONFIDENCE.POTENTIAL,
    custom_uri="/domain",
)

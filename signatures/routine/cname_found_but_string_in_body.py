from . import base

import signatures.generic

from detection_enums import CONFIDENCE


class cname_found_but_string_in_body(base.Base):
    def potential(self, domain, **kwargs) -> bool:
        return signatures.generic.CNAME.match(domain, self.cname)

    def check(self, domain, **kwargs) -> bool:
        if self.https:
            return signatures.generic.WEB.string_in_body_https(
                domain, self.domain_not_configured_message
            )
        return signatures.generic.WEB.string_in_body_http(
            domain, self.domain_not_configured_message
        )

    def __init__(
        self,
        cname,
        domain_not_configured_message,
        info,
        confidence=CONFIDENCE.CONFIRMED,
        https=False,
    ):
        self.cname = cname
        self.domain_not_configured_message = domain_not_configured_message
        self.https = https
        super().__init__(info, confidence)

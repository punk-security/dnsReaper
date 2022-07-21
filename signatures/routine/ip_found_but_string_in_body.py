from . import base

import signatures.generic

from detection_enums import CONFIDENCE

INFO = """
The defined domain has A/AAAA records configured for {service} and but a web request shows the domain is unclaimed. \
An attacker can register this domain on {service} and serve their own web content.
"""


class ip_found_but_string_in_body(base.Base):
    def potential(self, domain, **kwargs) -> bool:
        if signatures.generic.A.match(domain, self.ips):
            return True
        return signatures.generic.AAAA.match(domain, self.ips)

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
        ips,
        domain_not_configured_message,
        service,
        info=None,
        confidence=CONFIDENCE.CONFIRMED,
        https=False,
    ):
        self.ips = ips
        self.domain_not_configured_message = domain_not_configured_message
        self.https = https
        info = info if info else INFO
        super().__init__(info.format(service=service), confidence)

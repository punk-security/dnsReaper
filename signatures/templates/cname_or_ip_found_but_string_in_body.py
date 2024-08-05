from . import base

import signatures.checks

from detection_enums import CONFIDENCE

INFO = """
The defined domain has CNAME or A/AAAA records configured for {service} but a web request shows the domain is unclaimed. \
An attacker can register this domain on {service} and serve their own web content.
"""


class cname_or_ip_found_but_string_in_body(base.Base):
    def potential(self, domain, **kwargs) -> bool:
        return signatures.checks.COMBINED.matching_ip_or_cname(
            domain, self.cname, self.ips
        )

    async def check(self, domain, **kwargs) -> bool:
        if self.https:
            return await signatures.checks.WEB.string_in_body_https(
                domain, self.domain_not_configured_message, custom_uri=self.custom_uri
            )
        return await signatures.checks.WEB.string_in_body_http(
            domain, self.domain_not_configured_message, custom_uri=self.custom_uri
        )

    def __init__(
        self,
        cname,
        ips,
        domain_not_configured_message,
        service,
        info=None,
        https=False,
        custom_uri="",
        **kwargs
    ):
        self.cname = cname
        self.ips = ips
        self.domain_not_configured_message = domain_not_configured_message
        self.https = https
        self.custom_uri = custom_uri
        info = info if info else INFO
        super().__init__(info.format(service=service), **kwargs)

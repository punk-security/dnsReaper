from . import base

import signatures.checks

from detection_enums import CONFIDENCE

INFO = """
The defined domain has CNAME records configured for {service} but these records do not resolve. \
An attacker can register this domain on {service} and serve their own web content.
"""


class cname_found_but_NX_DOMAIN(base.Base):
    def potential(self, domain, **kwargs) -> bool:
        return signatures.checks.CNAME.match(domain, self.cname)

    async def check(self, domain, **kwargs) -> bool:
        return await signatures.checks.CNAME.NX_DOMAIN_on_resolve(domain)

    def __init__(self, cname, service, info=None, **kwargs):
        self.cname = cname
        info = info if info else INFO
        super().__init__(info.format(service=service), **kwargs)

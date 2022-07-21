from . import base

import signatures.generic

from detection_enums import CONFIDENCE


class cname_found_but_NX_DOMAIN(base.Base):
    def potential(self, domain, **kwargs) -> bool:
        return signatures.generic.CNAME.match(domain, self.cname)

    def check(self, domain, **kwargs) -> bool:
        return signatures.generic.CNAME.NX_DOMAIN_on_resolve(domain)

    def __init__(
        self,
        cname,
        info,
        confidence=CONFIDENCE.CONFIRMED,
    ):
        self.cname = cname
        super().__init__(info, confidence)

from . import base

import signatures.generic

from detection_enums import CONFIDENCE


class ns_found_but_no_SOA(base.Base):
    def potential(self, domain, **kwargs) -> bool:
        return signatures.generic.NS.match(domain, self.ns)

    def check(self, domain, **kwargs) -> bool:
        return signatures.generic.NS.no_SOA_detected(domain)

    def __init__(
        self,
        ns,
        info,
        confidence=CONFIDENCE.CONFIRMED,
    ):
        self.ns = ns
        super().__init__(info, confidence)

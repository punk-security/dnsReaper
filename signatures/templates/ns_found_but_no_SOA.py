from . import base

import signatures.checks

from detection_enums import CONFIDENCE

INFO = """
The defined domain has {service} NS records configured but these nameservers do not host a zone for this domain. \
An attacker can register this domain with {service} so they get provisioned onto a matching nameserver."""


class ns_found_but_no_SOA(base.Base):
    def potential(self, domain, **kwargs) -> bool:
        return signatures.checks.NS.match(domain, self.ns)

    async def check(self, domain, **kwargs) -> bool:
        return await signatures.checks.NS.no_SOA_detected(domain)

    def __init__(self, ns, service, sample_ns=None, info=None, **kwargs):
        self.ns = ns
        if sample_ns:
            self.sample_ns = sample_ns
        info = info if info else INFO
        super().__init__(info.format(service=service), **kwargs)

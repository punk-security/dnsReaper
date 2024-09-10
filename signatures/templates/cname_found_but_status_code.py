from . import base

import signatures.checks

from detection_enums import CONFIDENCE

INFO = """
The defined domain has a CNAME record configured for {service} but the website returns a {code}. \
You should investigate this 404 response.
    """


class cname_found_but_status_code(base.Base):
    def potential(self, domain, **kwargs) -> bool:
        return signatures.checks.CNAME.match(domain, self.cname)

    async def check(self, domain, **kwargs) -> bool:
        return await signatures.checks.WEB.status_code_match(
            domain, self.code, self.https
        )

    def __init__(self, cname, code, service, info=None, https=False, **kwargs):
        self.cname = cname
        self.https = https
        self.code = code
        if code < 10:
            code = f"{code}XX"
        info = info if info else INFO
        super().__init__(info.format(service=service, code=code), **kwargs)

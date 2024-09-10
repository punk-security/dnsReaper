from domain import Domain
from . import checks
import detection_enums

from .templates.base import Base


filtered_cname_substrings = [
    "elb.amazonaws.com",
    ".cloudfront.net",
    ".oracle.com",
    ".invalid",
    "online.lync.com",
]


def cname_should_be_filtered(cname):
    for f in filtered_cname_substrings:
        if f in cname:
            return True
    return False


def potential(domain: Domain, **kwargs) -> bool:
    if domain.CNAME != []:
        for cname in domain.CNAME:
            if cname_should_be_filtered(cname):
                continue
            if domain.domain in cname:
                # the entire domain is in the cname so its probably not customer provided input
                continue
            if domain.domain.split(".")[-2:] != cname.split(".")[-2:]:
                # last 2 parts of domain dont match, doesnt belong to same org
                return True
    return False


async def check(domain: Domain, **kwargs) -> bool:
    return await checks.CNAME.NX_DOMAIN_on_resolve(domain)


INFO = """
The defined domain has a CNAME record configured but the CNAME does not resolve. \
You should look to see if you can register or takeover this CNAME.
    """

test = Base(INFO, detection_enums.CONFIDENCE.POTENTIAL)
test.potential = potential
test.check = check

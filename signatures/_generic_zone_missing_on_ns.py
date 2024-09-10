from domain import Domain
from . import checks
import detection_enums

from .templates.base import Base


def potential(domain: Domain, **kwargs) -> bool:
    if domain.NS != []:
        for ns in domain.NS:
            if domain.domain.split(".")[-2:] != ns.split(".")[-2:]:
                # last 2 parts of domain dont match, otherwise belongs to same org
                return True
    return False


async def check(domain: Domain, **kwargs) -> bool:
    return await checks.NS.no_SOA_detected(domain)


INFO = """
The defined domain has NS records configured but these nameservers do not host a zone for this domain. \
An attacker may be able to register this domain on with the service managing the nameserver.
    """

test = Base(INFO, detection_enums.CONFIDENCE.POTENTIAL)
test.potential = potential
test.check = check

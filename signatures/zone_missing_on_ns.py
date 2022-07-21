from domain import Domain
from . import generic
import detection_enums

from .routine.base import Base


def potential(domain: Domain, **kwargs) -> bool:
    return domain.NS != []


def check(domain: Domain, **kwargs) -> bool:
    return generic.NS.no_SOA_detected(domain)


INFO = """
The defined domain has NS records configured but these nameservers do not host a zone for this domain. \
An attacker may be able to register this domain on with the service managing the nameserver.
    """

test = Base(INFO, detection_enums.CONFIDENCE.POTENTIAL)
test.potential = potential
test.check = check

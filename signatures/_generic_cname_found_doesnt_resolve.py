from domain import Domain
from . import checks
import detection_enums

from .templates.base import Base


def potential(domain: Domain, **kwargs) -> bool:
    return domain.CNAME != []


def check(domain: Domain, **kwargs) -> bool:
    return checks.CNAME.NX_DOMAIN_on_resolve(domain)


INFO = """
The defined domain has a CNAME record configured but the CNAME does not resolve. \
You should look to see if you can register or takeover this CNAME.
    """

test = Base(INFO, detection_enums.CONFIDENCE.POTENTIAL)
test.potential = potential
test.check = check

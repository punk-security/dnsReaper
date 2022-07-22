from domain import Domain
from . import generic
import detection_enums

from .routine.base import Base


def potential(domain: Domain, **kwargs) -> bool:
    return domain.CNAME != []


def check(domain: Domain, **kwargs) -> bool:
    return generic.CNAME.NX_DOMAIN_on_resolve(domain)


INFO = """
The defined domain has a CNAME record configured but the CNAME does not resolve. \
You should look to see if you can register or takeover this CNAME.
    """

test = Base(INFO, detection_enums.CONFIDENCE.UNLIKELY)
test.potential = potential
test.check = check

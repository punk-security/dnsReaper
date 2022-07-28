from domain import Domain
from . import checks
import detection_enums

from .templates.base import Base


def potential(domain: Domain, **kwargs) -> bool:
    if domain.CNAME != []:
        for cname in domain.CNAME:
            if cname.count(".") == 1:
                # This is a 2 part domain, i.e. foo.bar
                return True
    return False


def check(domain: Domain, **kwargs) -> bool:
    return checks.CNAME.is_unregistered(domain)


INFO = """
The defined domain has a CNAME record configured but the CNAME is not registered. \
You should look to see if you can register this CNAME.
    """

test = Base(INFO, detection_enums.CONFIDENCE.CONFIRMED)
test.potential = potential
test.check = check

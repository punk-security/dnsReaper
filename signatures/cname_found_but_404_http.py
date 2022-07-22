from domain import Domain
from . import generic
import detection_enums

from .routine.base import Base


def potential(domain: Domain, **kwargs) -> bool:
    return domain.CNAME != []


def check(domain: Domain, **kwargs) -> bool:
    return generic.WEB.status_code_404(domain, True)


INFO = """
The defined domain has a CNAME record configured but the website returns a 404 over HTTP. \
You should investigate this 404 response.
    """

test = Base(INFO, detection_enums.CONFIDENCE.UNLIKELY)
test.potential = potential
test.check = check

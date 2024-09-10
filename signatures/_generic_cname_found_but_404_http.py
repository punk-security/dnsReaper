from domain import Domain
from . import checks
import detection_enums

from .templates.base import Base


def potential(domain: Domain, **kwargs) -> bool:
    if domain.CNAME != []:
        for cname in domain.CNAME:
            if domain.domain.split(".")[-2:] != cname.split(".")[-2:]:
                # last 2 parts of domain dont match, doesnt belong to same org
                return True
    return False


async def check(domain: Domain, **kwargs) -> bool:
    return await checks.WEB.status_code_404(domain, False)


INFO = """
The defined domain has a CNAME record configured but the website returns a 404 over HTTP. \
You should investigate this 404 response.
    """

test = Base(INFO, detection_enums.CONFIDENCE.UNLIKELY)
test.potential = potential
test.check = check

from domain import Domain
from signatures import airee_ru

from tests import mocks


def test_check_ACTIVE():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_request_by_providing_static_host_resolution(
        domain, airee_ru.test.cname
    )
    assert airee_ru.test.check(domain) == True

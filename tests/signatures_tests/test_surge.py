from domain import Domain
from signatures import surge

from tests import mocks


def test_check_ACTIVE():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_request_by_providing_static_host_resolution(domain, surge.test.cname)
    assert surge.test.check(domain) == True

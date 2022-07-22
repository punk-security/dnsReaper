from domain import Domain
from signatures import bigcartel

from tests import mocks


def test_check_ACTIVE():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_request_by_providing_static_host_resolution(
        domain, bigcartel.test.cname
    )
    assert bigcartel.test.check(domain) == True

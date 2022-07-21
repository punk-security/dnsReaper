from domain import Domain
from signatures import wordpress_com_cname

from tests import mocks


def test_check_ACTIVE():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_request_by_providing_static_host_resolution(
        domain, "mysite.wordpress.com"
    )
    assert wordpress_com_cname.test.check(domain) == True

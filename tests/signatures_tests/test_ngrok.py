from domain import Domain
from signatures import ngrok

from tests import mocks


def test_check_ACTIVE():
    for cname in ngrok.test.cname:
        domain = Domain("mock.local", fetch_standard_records=False)
        mocks.mock_web_request_by_providing_static_host_resolution(domain, cname)
        assert ngrok.test.check(domain) == True

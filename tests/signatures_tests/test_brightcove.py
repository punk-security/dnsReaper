from domain import Domain
from signatures import brightcove
from tests import mocks
from uuid import uuid1


def test_check_success_ACTIVE():
    for cname in brightcove.test.cname:
        domain = Domain(f"{uuid1().hex}.com", fetch_standard_records=False)
        mocks.mock_web_request_by_providing_static_host_resolution(
            domain, f"{uuid1().hex}{cname}"
        )
        assert brightcove.test.check(domain) == True

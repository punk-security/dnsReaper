from domain import Domain
from signatures import wordpress_com_cname

import mocks


def test_potential_success_with_matching_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["goose.wordpress.com"]
    assert wordpress_com_cname.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert wordpress_com_cname.potential(domain) == False


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_response_with_static_value(
        domain, wordpress_com_cname.domain_not_configured_message
    )
    assert wordpress_com_cname.check(domain) == True


def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_response_with_static_value(domain, "Welcome to my blog!")
    assert wordpress_com_cname.check(domain) == False


def test_check_ACTIVE():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_request_by_providing_static_host_resolution(
        domain, wordpress_com_cname.wordpress_cname
    )
    assert wordpress_com_cname.check(domain) == True

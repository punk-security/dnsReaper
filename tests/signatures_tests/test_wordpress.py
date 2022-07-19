from domain import Domain
from signatures import wordpress_com

import mocks


def test_potential_success_with_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    for ns in wordpress_com.wordpress_ns:
        domain.NS = [ns]
    assert wordpress_com.potential(domain) == True


def test_potential_success_with_matching_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["goose.wordpress.com"]
    assert wordpress_com.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert wordpress_com.potential(domain) == False


def test_check_success():
    domain = mocks.mock_web_response(wordpress_com.domain_not_configured_message)
    assert wordpress_com.check(domain) == True


def test_check_failure():
    domain = mocks.mock_web_response("Welcome to my blog!")
    assert wordpress_com.check(domain) == False

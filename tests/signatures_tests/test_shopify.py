from domain import Domain
from signatures import shopify

from tests import mocks


def test_potential_success_match_ipv4():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = [shopify.shopify_ipv4]
    assert shopify.potential(domain) == True


def test_potential_success_match_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = [shopify.shopify_cname]
    assert shopify.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert shopify.potential(domain) == False


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_response_with_static_value(
        domain, shopify.domain_not_configured_message
    )
    assert shopify.check(domain) == True


def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_response_with_static_value(domain, "Welcome to my shop!")
    assert shopify.check(domain) == False


def test_check_message_for_ipv4_ACTIVE():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_request_by_providing_static_host_resolution(
        domain, shopify.shopify_ipv4
    )
    assert shopify.check(domain) == True


def test_check_message_for_cname_ACTIVE():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_request_by_providing_static_host_resolution(
        domain, shopify.shopify_cname
    )
    assert shopify.check(domain) == True

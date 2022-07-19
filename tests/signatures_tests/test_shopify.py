from domain import Domain
from signatures import shopify
import mocks


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
    domain = mocks.mock_web_response(shopify.domain_not_configured_message)
    assert shopify.check(domain) == True


def test_check_failure():
    domain = mocks.mock_web_response("Welcome to my shop!")
    assert shopify.check(domain) == False

from domain import Domain
from signatures import shopify

from collections import namedtuple


def test_potential_success_match_ipv4():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = [shopify.shopify_ipv4]
    assert shopify.potential(domain) == True


def test_potential_success_match_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = [shopify.shopify_cname]
    assert shopify.potential(domain) == True


def test_potential_success_match_ipv4_from_multiple():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", shopify.shopify_ipv4]
    assert shopify.potential(domain) == True


def test_potential_fail_no_A_or_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert shopify.potential(domain) == False


def test_potential_fail_no_matching():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1"]
    domain.CNAME = ["cname"]
    assert shopify.potential(domain) == False


def test_check_success():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(
            shopify.domain_not_configured_message
        )

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert shopify.check(domain) == True


def test_check_fail_working_store():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])("Welcome to my store!")

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert shopify.check(domain) == False


def test_check_fail_no_response():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code", "body"])(0, "")

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert shopify.check(domain) == False

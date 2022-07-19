from domain import Domain
from signatures import github_pages
import mocks


def test_potential_success_match_ipv4():
    domain = Domain("mock.local", fetch_standard_records=False)
    for ip in github_pages.github_pages_ipv4:
        domain.A = ip
        assert github_pages.potential(domain) == True


def test_potential_success_match_ipv6():
    domain = Domain("mock.local", fetch_standard_records=False)
    for ip in github_pages.github_pages_ipv6:
        domain.AAAA = ip
        assert github_pages.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert github_pages.potential(domain) == False


def test_check_success():
    domain = mocks.mock_web_response(github_pages.domain_not_configured_message)
    assert github_pages.check(domain) == True


def test_check_failure():
    domain = mocks.mock_web_response("Welcome to my github pages!")
    assert github_pages.check(domain) == False

from domain import Domain
from signatures import github_pages

from collections import namedtuple


def test_potential_success_one_match_ipv4():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = [github_pages.github_pages_ipv4[0]]
    assert github_pages.potential(domain) == True


def test_potential_success_one_match_from_multiple_ipv4():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", github_pages.github_pages_ipv4[0]]
    assert github_pages.potential(domain) == True


def test_potential_success_all_match_ipv4():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = github_pages.github_pages_ipv4
    assert github_pages.potential(domain) == True


def test_potential_success_one_match_ipv6():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = [github_pages.github_pages_ipv6[0]]
    assert github_pages.potential(domain) == True


def test_potential_success_all_match_ipv6():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = github_pages.github_pages_ipv6
    assert github_pages.potential(domain) == True


def test_potential_fail_no_A_or_AAAA():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert github_pages.potential(domain) == False


def test_potential_fail_no_matching():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1"]
    domain.AAAA = ["::1"]
    assert github_pages.potential(domain) == False


def test_check_success():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(404)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert github_pages.check(domain) == True


def test_check_fail():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(200)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert github_pages.check(domain) == False

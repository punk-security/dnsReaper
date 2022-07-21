from domain import Domain
from signatures import github_pages

from tests import mocks


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


def test_check_message_ACTIVE():
    for ip in github_pages.github_pages_ipv4:  # no ipv6 for tests as no one has it
        domain = Domain("mock.local", fetch_standard_records=False)
        mocks.mock_web_request_by_providing_static_host_resolution(domain, ip)
        assert github_pages.check(domain) == True

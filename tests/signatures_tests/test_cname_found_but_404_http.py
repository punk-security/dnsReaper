from domain import Domain
from signatures import cname_found_but_404_http

from collections import namedtuple


def test_potential_success_with_a_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    assert cname_found_but_404_http.test.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert cname_found_but_404_http.test.potential(domain) == False


def test_check_success():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(404)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert cname_found_but_404_http.test.check(domain) == True


def test_check_failure():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(200)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert cname_found_but_404_http.test.check(domain) == False

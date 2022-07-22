from domain import Domain
from signatures import cname_found_doesnt_resolve
from unittest.mock import patch, PropertyMock


def test_potential_success_with_a_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    assert cname_found_doesnt_resolve.test.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert cname_found_doesnt_resolve.test.potential(domain) == False


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("domain.Domain.query", return_value=[]):
        assert cname_found_doesnt_resolve.test.check(domain) == True


def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("domain.Domain.query", return_value=["something"]):
        assert cname_found_doesnt_resolve.test.check(domain) == False

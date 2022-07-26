from domain import Domain
from signatures import _generic_cname_found_doesnt_resolve
from unittest.mock import patch
from tests import mocks


def test_potential_success_with_a_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    assert _generic_cname_found_doesnt_resolve.test.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert _generic_cname_found_doesnt_resolve.test.potential(domain) == False


def test_potential_failure_with_same_root_For_both_domain_and_cname():
    domain = Domain("foo.mock.local", fetch_standard_records=False)
    domain.CNAME = ["bar.mock.local"]
    assert _generic_cname_found_doesnt_resolve.test.potential(domain) == False


def test_potential_failure_with_filtered_cname():
    for cname in _generic_cname_found_doesnt_resolve.filtered_cname_substrings:
        domain = Domain("foo.mock.local", fetch_standard_records=False)
        domain.CNAME = [cname]
        assert _generic_cname_found_doesnt_resolve.test.potential(domain) == False


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("domain.Domain.query", return_value=[]):
        assert _generic_cname_found_doesnt_resolve.test.check(domain) == True


def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("domain.Domain.query", return_value=["something"]):
        assert _generic_cname_found_doesnt_resolve.test.check(domain) == False


def test_check_success_ACTIVE():
    test_cname = f"{mocks.random_string()}.io"
    domain = Domain(f"{mocks.random_string()}.com", fetch_standard_records=False)
    domain.CNAME = [test_cname]
    print(f"Testing cname {test_cname}")
    assert _generic_cname_found_doesnt_resolve.test.check(domain) == True

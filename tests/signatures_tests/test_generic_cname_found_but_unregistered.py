from domain import Domain
from signatures import _generic_cname_found_but_unregistered
from unittest.mock import patch, PropertyMock
from tests import mocks


def test_potential_success_with_a_cname_of_two_parts():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname.tld"]
    assert _generic_cname_found_but_unregistered.test.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert _generic_cname_found_but_unregistered.test.potential(domain) == False


def test_potential_failure_with_three_part_domain():
    domain = Domain("foo.mock.local", fetch_standard_records=False)
    domain.CNAME = ["subdomain.cname.tld"]
    assert _generic_cname_found_but_unregistered.test.potential(domain) == False


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname.tld"]
    with patch(
        "domain.Domain.is_registered", return_value=False, new_callable=PropertyMock
    ):
        assert _generic_cname_found_but_unregistered.test.check(domain) == True


def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname.tld"]
    with patch(
        "domain.Domain.is_registered", return_value=True, new_callable=PropertyMock
    ):
        assert _generic_cname_found_but_unregistered.test.check(domain) == False


def test_check_success_ACTIVE():
    test_cname = f"{mocks.random_string()}.io"
    domain = Domain(f"{mocks.random_string()}.com", fetch_standard_records=False)
    domain.CNAME = [test_cname]
    print(f"Testing cname {test_cname}")
    assert _generic_cname_found_but_unregistered.test.check(domain) == True

from domain import Domain
from signatures.routine.cname_found_but_NX_DOMAIN import (
    cname_found_but_NX_DOMAIN,
)

from tests import mocks
from unittest.mock import patch, PropertyMock

test = cname_found_but_NX_DOMAIN("cname", "INFO")


def test_potential_success_with_matching_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    assert test.potential(domain) == True


def test_potential_failure_no_matching_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert test.potential(domain) == False


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("domain.Domain.query", return_value=[]):
        assert test.check(domain) == True


def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("domain.Domain.query", return_value=["something"]):
        assert test.check(domain) == False

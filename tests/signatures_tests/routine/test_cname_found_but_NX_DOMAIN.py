from domain import Domain
import signatures
from signatures.routine.cname_found_but_NX_DOMAIN import (
    cname_found_but_NX_DOMAIN,
)

from tests import mocks
from unittest.mock import patch
import pytest

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


signatures = [getattr(signatures, signature) for signature in signatures.__all__]


@pytest.mark.parametrize(
    "signature",
    [s for s in signatures if isinstance(s.test, cname_found_but_NX_DOMAIN)],
)
def test_check_success_ACTIVE(signature):
    cnames = (
        signature.test.cname
        if type(signature.test.cname) == list
        else [signature.test.cname]
    )
    for cname in cnames:
        test_cname = f"{mocks.random_string()}{cname}" if cname[0] == "." else cname
        domain = Domain(f"{mocks.random_string()}.com", fetch_standard_records=False)
        domain.CNAME = [test_cname]
        print(f"Testing cname {test_cname}")
        assert signature.test.check(domain) == True

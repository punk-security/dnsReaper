from domain import Domain
from signatures import _generic_cname_found_doesnt_resolve
from unittest.mock import patch
from .. import mocks
import pytest


@pytest.mark.asyncio
async def test_potential_success_with_a_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    assert _generic_cname_found_doesnt_resolve.test.potential(domain) == True


@pytest.mark.asyncio
async def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert _generic_cname_found_doesnt_resolve.test.potential(domain) == False


@pytest.mark.asyncio
async def test_potential_failure_with_same_root_For_both_domain_and_cname():
    domain = Domain("foo.mock.local", fetch_standard_records=False)
    domain.CNAME = ["bar.mock.local"]
    assert _generic_cname_found_doesnt_resolve.test.potential(domain) == False


@pytest.mark.asyncio
async def test_potential_failure_with_filtered_cname():
    for cname in _generic_cname_found_doesnt_resolve.filtered_cname_substrings:
        domain = Domain("foo.mock.local", fetch_standard_records=False)
        domain.CNAME = [cname]
        assert _generic_cname_found_doesnt_resolve.test.potential(domain) == False


@pytest.mark.asyncio
async def test_potential_failure_with_domain_in_cname():
    domain = Domain("foo.mock.local", fetch_standard_records=False)
    domain.CNAME = ["foo.mock.local.cdn"]
    assert _generic_cname_found_doesnt_resolve.test.potential(domain) == False


@pytest.mark.asyncio
async def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("resolver.Resolver.resolve", return_value={"NX_DOMAIN": True}):
        assert (await _generic_cname_found_doesnt_resolve.test.check(domain)) == True


@pytest.mark.asyncio
async def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("resolver.Resolver.resolve", return_value={"NX_DOMAIN": False}):
        assert (await _generic_cname_found_doesnt_resolve.test.check(domain)) == False


@pytest.mark.asyncio
async def test_check_success_ACTIVE():
    test_cname = f"{mocks.random_string()}.io"
    domain = Domain(f"{mocks.random_string()}.com", fetch_standard_records=False)
    domain.CNAME = [test_cname]
    print(f"Testing cname {test_cname}")
    assert (await _generic_cname_found_doesnt_resolve.test.check(domain)) == True

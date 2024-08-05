from domain import Domain
import signatures
from signatures.templates.cname_found_but_NX_DOMAIN import (
    cname_found_but_NX_DOMAIN,
)

from ... import mocks
from unittest.mock import patch
import pytest

test = cname_found_but_NX_DOMAIN("cname", "INFO")


@pytest.mark.asyncio
async def test_potential_success_with_matching_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    assert test.potential(domain) == True


@pytest.mark.asyncio
async def test_potential_failure_no_matching_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert test.potential(domain) == False


@pytest.mark.asyncio
async def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("resolver.Resolver.resolve", return_value={"NX_DOMAIN": True}):
        assert await test.check(domain) == True


@pytest.mark.asyncio
async def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    with patch("resolver.Resolver.resolve", return_value={"NX_DOMAIN": False}):
        assert await test.check(domain) == False


signatures = [getattr(signatures, signature) for signature in signatures.__all__]


@pytest.mark.parametrize(
    "signature",
    [s for s in signatures if isinstance(s.test, cname_found_but_NX_DOMAIN)],
)
@pytest.mark.asyncio
async def test_check_success_ACTIVE(signature):
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
        assert await signature.test.check(domain) == True

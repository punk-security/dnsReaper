from domain import Domain
from signatures import _generic_cname_found_but_unregistered
from unittest.mock import patch, PropertyMock, AsyncMock
from .. import mocks
import pytest


@pytest.mark.asyncio
async def test_potential_success_with_a_cname_of_two_parts():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname.tld"]
    assert _generic_cname_found_but_unregistered.test.potential(domain) == True


@pytest.mark.asyncio
async def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert _generic_cname_found_but_unregistered.test.potential(domain) == False


@pytest.mark.asyncio
async def test_potential_failure_with_three_part_domain():
    domain = Domain("foo.mock.local", fetch_standard_records=False)
    domain.CNAME = ["subdomain.cname.tld"]
    assert _generic_cname_found_but_unregistered.test.potential(domain) == False


@pytest.mark.asyncio
async def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname.tld"]
    with patch(
        "domain.Domain.is_registered",
        new=PropertyMock(spec=AsyncMock()(), return_value=False),
    ) as mock:
        assert await _generic_cname_found_but_unregistered.test.check(domain) == True
        assert mock.await_count == 1


@pytest.mark.asyncio
async def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname.tld"]
    with patch(
        "domain.Domain.is_registered",
        new=PropertyMock(spec=AsyncMock()(), return_value=True),
    ) as mock:
        assert await _generic_cname_found_but_unregistered.test.check(domain) == False
        assert mock.await_count == 1


@pytest.mark.asyncio
async def test_check_success_ACTIVE():
    test_cname = f"{mocks.random_string()}.co.uk"
    domain = Domain(f"{mocks.random_string()}.com", fetch_standard_records=False)
    domain.CNAME = [test_cname]
    print(f"Testing cname {test_cname}")
    assert await _generic_cname_found_but_unregistered.test.check(domain) == True

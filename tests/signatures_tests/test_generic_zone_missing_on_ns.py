from domain import Domain
from signatures import _generic_zone_missing_on_ns
import pytest


@pytest.mark.asyncio
async def test_potential_success_with_a_nameserver():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    assert _generic_zone_missing_on_ns.test.potential(domain) == True


@pytest.mark.asyncio
async def test_potential_success_with_multiple_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns1", "ns2"]
    assert _generic_zone_missing_on_ns.test.potential(domain) == True


@pytest.mark.asyncio
async def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert _generic_zone_missing_on_ns.test.potential(domain) == False


@pytest.mark.asyncio
async def test_potential_failure_with_same_root_for_both_domain_and_ns():
    domain = Domain("something.mock.local", fetch_standard_records=False)
    domain.NS = ["ns1.mock.local"]
    assert _generic_zone_missing_on_ns.test.potential(domain) == False

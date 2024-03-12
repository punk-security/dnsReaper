from domain import Domain
from signatures.checks import AAAA
import pytest


@pytest.mark.asyncio
async def test_ipv6_in_AAAA_for_single_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert AAAA.match(domain, "::1") == True


@pytest.mark.asyncio
async def test_ipv6_in_AAAA_for_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert AAAA.match(domain, ["::1", "::2"]) == True


@pytest.mark.asyncio
async def test_ipv6_in_AAAA_for_one_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::3"]
    assert AAAA.match(domain, ["::1", "::2"]) == True


@pytest.mark.asyncio
async def test_ipv6_in_AAAA_for_none_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert AAAA.match(domain, ["::3", "::4"]) == False


@pytest.mark.asyncio
async def test_ipv6_in_AAAA_for_none_matching_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert AAAA.match(domain, "::3") == False


@pytest.mark.asyncio
async def test_ipv6_in_AAAA_with_no_AAAA_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = []
    assert AAAA.match(domain, "::1") == False


@pytest.mark.asyncio
async def test_ipv6_in_AAAA_multiple_with_no_AAAA_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = []
    assert AAAA.match(domain, ["::1", "::2"]) == False

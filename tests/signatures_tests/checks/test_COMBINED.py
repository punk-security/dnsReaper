from xml import dom
from domain import Domain
from signatures.checks import COMBINED
import pytest


## matching_ipv4_or_ipv6
@pytest.mark.asyncio
async def test_matching_ipv4_or_ipv6_ipv4_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1"]
    domain.AAAA = []
    assert COMBINED.matching_ipv4_or_ipv6(domain, "1.1.1.1", "::1") == True


@pytest.mark.asyncio
async def test_matching_ipv4_or_ipv6_ipv6_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.AAAA = ["::1"]
    assert COMBINED.matching_ipv4_or_ipv6(domain, "1.1.1.1", "::1") == True


@pytest.mark.asyncio
async def test_matching_ipv4_or_ipv6_no_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.AAAA = []
    assert COMBINED.matching_ipv4_or_ipv6(domain, "1.1.1.1", "::1") == False


## macthing_ip_or_cname
@pytest.mark.asyncio
async def test_matching_ip_or_cname_single_ipv4_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1"]
    domain.CNAME = []
    assert COMBINED.matching_ip_or_cname(domain, "", ips="1.1.1.1") == True


@pytest.mark.asyncio
async def test_matching_ip_or_cname_multiple_ipv4_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["2.2.2.2"]
    domain.CNAME = []
    assert COMBINED.matching_ip_or_cname(domain, "", ips=["1.1.1.1", "2.2.2.2"]) == True


@pytest.mark.asyncio
async def test_matching_ip_or_cname_single_ipv6_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1"]
    domain.CNAME = []
    assert COMBINED.matching_ip_or_cname(domain, "", ips="::1") == True


@pytest.mark.asyncio
async def test_matching_ip_or_cname_multiple_ipv6_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::2"]
    domain.CNAME = []
    assert COMBINED.matching_ip_or_cname(domain, "", ips=["::1", "::2"]) == True


@pytest.mark.asyncio
async def test_matching_ip_or_cname_multiple_ips_match_ipv6():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::2"]
    domain.CNAME = []
    assert COMBINED.matching_ip_or_cname(domain, "", ips=["1.1.1.1", "::2"]) == True


@pytest.mark.asyncio
async def test_matching_ip_or_cname_multiple_ips_match_ipv4():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1"]
    domain.CNAME = []
    assert COMBINED.matching_ip_or_cname(domain, "", ips=["1.1.1.1", "::2"]) == True


@pytest.mark.asyncio
async def test_matching_ip_or_cname_cname_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.CNAME = ["goose"]
    assert (
        COMBINED.matching_ip_or_cname(domain, "goose", ips=["1.1.1.1", "::1"]) == True
    )


@pytest.mark.asyncio
async def test_matching_ip_or_cname_no_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.AAAA = []
    domain.CNAME = []
    assert (
        COMBINED.matching_ip_or_cname(domain, "goose", ips=["1.1.1.1", "::1"]) == False
    )


## macthing_ipv4_or_cname
@pytest.mark.asyncio
async def test_matching_ipv4_or_cname_ipv4_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1"]
    domain.CNAME = []
    assert COMBINED.matching_ipv4_or_cname(domain, "1.1.1.1", "goose") == True


@pytest.mark.asyncio
async def test_matching_ipv4_or_cname_cname_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.CNAME = ["goose"]
    assert COMBINED.matching_ipv4_or_cname(domain, "1.1.1.1", "goose") == True


@pytest.mark.asyncio
async def test_matching_ipv4_or_cname_no_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.AAAA = []
    assert COMBINED.matching_ipv4_or_cname(domain, "1.1.1.1", "goose") == False

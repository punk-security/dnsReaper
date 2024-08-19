from domain import Domain
from signatures.checks import NS
from unittest.mock import patch, PropertyMock
import pytest


@pytest.mark.asyncio
async def test_match_for_single_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, "abc") == True


@pytest.mark.asyncio
async def test_match_for_single_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, "b") == True


@pytest.mark.asyncio
async def test_match_where_ns_is_subtring_of_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, "abcd") == False


@pytest.mark.asyncio
async def test_match_for_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, ["abc", "def"]) == True


@pytest.mark.asyncio
async def test_match_for_one_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "hij"]
    assert NS.match(domain, ["abc", "def"]) == True


@pytest.mark.asyncio
async def test_match_for_one_of_multiple_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "hij"]
    assert NS.match(domain, ["def", "h"]) == True


@pytest.mark.asyncio
async def test_match_for_none_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, ["hij", "klm"]) == False


@pytest.mark.asyncio
async def test_match_for_none_matching_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, "hij") == False


@pytest.mark.asyncio
async def test_match_with_no_ns_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = []
    assert NS.match(domain, "abc") == False


@pytest.mark.asyncio
async def test_match_multiple_with_no_ns_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = []
    assert NS.match(domain, ["abc", "def"]) == False


@pytest.mark.asyncio
async def test_no_SOA_detected_on_NS_with_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch("resolver.Resolver.resolve_with_ns", return_value={"SOA": []}):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert (await NS.no_SOA_detected(domain)) == True


@pytest.mark.asyncio
async def test_no_SOA_detected_on_NS_with_no_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]

    with patch(
        "resolver.Resolver.resolve_with_ns", return_value={"SOA": ["SOA RECORD HERE"]}
    ):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert (await NS.no_SOA_detected(domain)) == False


@pytest.mark.asyncio
async def test_no_SOA_detected_on_NS_with_no_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = []
    assert (await NS.no_SOA_detected(domain)) == False

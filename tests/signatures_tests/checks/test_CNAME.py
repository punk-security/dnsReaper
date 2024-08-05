from domain import Domain
from signatures.checks import CNAME
from unittest.mock import patch, AsyncMock
from asyncwhois.errors import NotFoundError
from ... import mocks
import pytest


@pytest.mark.asyncio
async def test_match_for_single_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, "abc") == True


@pytest.mark.asyncio
async def test_match_for_single_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, "b") == True


@pytest.mark.asyncio
async def test_match_where_cname_is_subtring_of_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, "abcd") == False


@pytest.mark.asyncio
async def test_match_for_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, ["abc", "def"]) == True


@pytest.mark.asyncio
async def test_match_for_one_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "hij"]
    assert CNAME.match(domain, ["abc", "def"]) == True


@pytest.mark.asyncio
async def test_match_for_one_of_multiple_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "hij"]
    assert CNAME.match(domain, ["def", "h"]) == True


@pytest.mark.asyncio
async def test_match_for_none_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, ["hij", "klm"]) == False


@pytest.mark.asyncio
async def test_match_for_none_matching_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, "hij") == False


@pytest.mark.asyncio
async def test_match_with_no_CNAME_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = []
    assert CNAME.match(domain, "abc") == False


@pytest.mark.asyncio
async def test_match_multiple_with_no_CNAME_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = []
    assert CNAME.match(domain, ["abc", "def"]) == False


## NX_DOMAIN_on_resolve

domain_with_cname = Domain("mock.local", fetch_standard_records=False)
domain_with_cname.CNAME = ["cname"]


@pytest.mark.asyncio
async def test_NX_DOMAIN_on_resolve_success():
    with patch(
        "resolver.Resolver.resolve",
        side_effect=AsyncMock(return_value={"NX_DOMAIN": True}),
    ):
        assert await CNAME.NX_DOMAIN_on_resolve(domain_with_cname) == True


@pytest.mark.asyncio
async def test_NX_DOMAIN_on_resolve_failure_no_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    with patch(
        "resolver.Resolver.resolve",
        side_effect=AsyncMock(return_value={"NX_DOMAIN": False}),
    ):
        assert await CNAME.NX_DOMAIN_on_resolve(domain_with_cname) == False


@pytest.mark.asyncio
async def test_is_unregistered_failure_no_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert await CNAME.is_unregistered(domain) == False


@pytest.mark.asyncio
async def test_is_unregistered_failure_cname_registered():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["something"]
    with patch(
        "domain.asyncwhois.aio_whois",
        side_effect=AsyncMock(return_value={"registrar": "something"}),
    ):
        assert await CNAME.is_unregistered(domain) == False


@pytest.mark.asyncio
async def test_is_unregistered_failure_whois_failure():
    async def whois(domain):
        raise ValueError("BOOK")

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["something"]
    with patch("domain.asyncwhois.aio_whois", new=whois):
        assert await CNAME.is_unregistered(domain) == False


@pytest.mark.asyncio
async def test_is_unregistered_success_cname_unregistered():
    async def whois(domain):
        raise NotFoundError("Domain not found!")

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["something"]
    with patch("domain.asyncwhois.aio_whois", new=whois):
        assert await CNAME.is_unregistered(domain) == True


@pytest.mark.asyncio
async def test_is_unregistered_success_cname_unregistered_ACTIVE():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = [f"{mocks.random_string()}.com"]
    assert await CNAME.is_unregistered(domain) == True

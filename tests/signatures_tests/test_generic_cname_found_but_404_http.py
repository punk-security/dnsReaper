from domain import Domain
from signatures import _generic_cname_found_but_404_http

from collections import namedtuple
import pytest


@pytest.mark.asyncio
async def test_potential_success_with_a_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["cname"]
    assert _generic_cname_found_but_404_http.test.potential(domain) == True


@pytest.mark.asyncio
async def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert _generic_cname_found_but_404_http.test.potential(domain) == False


@pytest.mark.asyncio
async def test_potential_failure_with_same_root_For_both_domain_and_cname():
    domain = Domain("foo.mock.local", fetch_standard_records=False)
    domain.CNAME = ["bar.mock.local"]
    assert _generic_cname_found_but_404_http.test.potential(domain) == False


@pytest.mark.asyncio
async def test_check_success():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(404)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await _generic_cname_found_but_404_http.test.check(domain) == True


@pytest.mark.asyncio
async def test_check_failure():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(200)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await _generic_cname_found_but_404_http.test.check(domain) == False

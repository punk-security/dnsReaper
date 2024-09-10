from domain import Domain
from signatures.checks import WEB

from collections import namedtuple

import pytest

## string_in_body

string_in_body_response = "This is a response"
string_in_body_full_match = "This is a response"
string_in_body_partial_match = "response"
string_in_body_no_match = "goose"


@pytest.mark.asyncio
async def test_string_in_body_success_on_full_match():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.string_in_body(domain, string_in_body_full_match, False) == True


@pytest.mark.asyncio
async def test_string_in_body_success_on_partial_match():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.string_in_body(domain, string_in_body_partial_match, False) == True


@pytest.mark.asyncio
async def test_string_in_body_failure_on_no_match():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.string_in_body(domain, string_in_body_no_match, False) == False


@pytest.mark.asyncio
async def test_string_in_body_failure_on_no_body():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])("")

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.string_in_body(domain, string_in_body_full_match, False) == False


## status_code_match


@pytest.mark.asyncio
async def test_status_code_match_success_specific():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(200)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.status_code_match(domain, 200, False) == True


@pytest.mark.asyncio
async def test_status_code_match_success_partial():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(302)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.status_code_match(domain, 3, False) == True


@pytest.mark.asyncio
async def test_status_code_match_fail_specific():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(302)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.status_code_match(domain, 401, False) == False


@pytest.mark.asyncio
async def test_status_code_match_fail_partial():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(404)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.status_code_match(domain, 3, False) == False


@pytest.mark.asyncio
async def test_status_code_match_fail_partial():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(404)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.status_code_match(domain, 3, False) == False


@pytest.mark.asyncio
async def test_status_code_404_success():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(404)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.status_code_404(domain, False) == True


@pytest.mark.asyncio
async def test_status_code_404_failure():
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(200)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert await WEB.status_code_404(domain, False) == False

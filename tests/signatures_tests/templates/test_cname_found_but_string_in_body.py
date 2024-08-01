from domain import Domain
import signatures
from signatures.templates.cname_found_but_string_in_body import (
    cname_found_but_string_in_body,
)

from ... import mocks
import pytest

test = cname_found_but_string_in_body("cname", "No domain found here", "INFO")


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
    mocks.mock_web_response_with_static_value(
        domain, test.domain_not_configured_message
    )
    assert await test.check(domain) == True


@pytest.mark.asyncio
async def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    mocks.mock_web_response_with_static_value(domain, "Welcome to my site!")
    assert await test.check(domain) == False


signatures = [getattr(signatures, signature) for signature in signatures.__all__]


@pytest.mark.parametrize(
    "signature",
    [s for s in signatures if isinstance(s.test, cname_found_but_string_in_body)],
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
        domain.get_session = (
            mocks.generate_mock_aiohttp_session_with_forced_cname_resolution(test_cname)
        )
        assert await signature.test.check(domain) == True

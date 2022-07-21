from domain import Domain
import signatures.generic

from collections import namedtuple

## string_in_body

string_in_body_response = "This is a response"
string_in_body_full_match = "This is a response"
string_in_body_partial_match = "response"
string_in_body_no_match = "goose"


def test_check_string_in_body_success_on_full_match():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert (
        signatures.generic.WEB.string_in_body(domain, string_in_body_full_match, False)
        == True
    )


def test_check_string_in_body_success_on_partial_match():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert (
        signatures.generic.WEB.string_in_body(
            domain, string_in_body_partial_match, False
        )
        == True
    )


def test_check_string_in_body_failure_on_no_match():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert (
        signatures.generic.WEB.string_in_body(domain, string_in_body_no_match, False)
        == False
    )


def test_check_string_in_body_failure_on_no_body():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])("")

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert (
        signatures.generic.WEB.string_in_body(domain, string_in_body_full_match, False)
        == False
    )

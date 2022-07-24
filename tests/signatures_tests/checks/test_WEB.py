from domain import Domain
from signatures.checks import WEB

from collections import namedtuple

## string_in_body

string_in_body_response = "This is a response"
string_in_body_full_match = "This is a response"
string_in_body_partial_match = "response"
string_in_body_no_match = "goose"


def test_string_in_body_success_on_full_match():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.string_in_body(domain, string_in_body_full_match, False) == True


def test_string_in_body_success_on_partial_match():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.string_in_body(domain, string_in_body_partial_match, False) == True


def test_string_in_body_failure_on_no_match():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.string_in_body(domain, string_in_body_no_match, False) == False


def test_string_in_body_failure_on_no_body():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])("")

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.string_in_body(domain, string_in_body_full_match, False) == False


## status_code_match


def test_status_code_match_success_specific():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(200)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.status_code_match(domain, 200, False) == True


def test_status_code_match_success_partial():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(302)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.status_code_match(domain, 3, False) == True


def test_status_code_match_fail_specific():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(302)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.status_code_match(domain, 401, False) == False


def test_status_code_match_fail_partial():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(404)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.status_code_match(domain, 3, False) == False


def test_status_code_match_fail_partial():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(404)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.status_code_match(domain, 3, False) == False


def test_status_code_404_success():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(404)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.status_code_404(domain, False) == True


def test_status_code_404_failure():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["status_code"])(200)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert WEB.status_code_404(domain, False) == False

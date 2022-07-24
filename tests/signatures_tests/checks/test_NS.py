from domain import Domain
from signatures.checks import NS
from unittest.mock import patch, PropertyMock


def test_match_for_single_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, "abc") == True


def test_match_for_single_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, "b") == True


def test_match_where_ns_is_subtring_of_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, "abcd") == False


def test_match_for_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, ["abc", "def"]) == True


def test_match_for_one_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "hij"]
    assert NS.match(domain, ["abc", "def"]) == True


def test_match_for_one_of_multiple_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "hij"]
    assert NS.match(domain, ["def", "h"]) == True


def test_match_for_none_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, ["hij", "klm"]) == False


def test_match_for_none_matching_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert NS.match(domain, "hij") == False


def test_match_with_no_ns_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = []
    assert NS.match(domain, "abc") == False


def test_match_multiple_with_no_ns_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = []
    assert NS.match(domain, ["abc", "def"]) == False


def test_no_SOA_detected_on_NS_with_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch("domain.Domain.SOA", return_value=[], new_callable=PropertyMock):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert NS.no_SOA_detected(domain) == True


def test_no_SOA_detected_on_NS_with_no_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch(
        "domain.Domain.SOA", return_value=["SOA RECORD HERE"], new_callable=PropertyMock
    ):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert NS.no_SOA_detected(domain) == False


def test_no_SOA_detected_on_NS_with_no_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = []
    assert NS.no_SOA_detected(domain) == False

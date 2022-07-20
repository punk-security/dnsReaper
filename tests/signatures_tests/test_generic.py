from domain import Domain
import generic_checks

from collections import namedtuple

from unittest.mock import patch, PropertyMock

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
        generic_checks.string_in_body(domain, string_in_body_full_match, False) == True
    )


def test_check_string_in_body_success_on_partial_match():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert (
        generic_checks.string_in_body(domain, string_in_body_partial_match, False)
        == True
    )


def test_check_string_in_body_failure_on_no_match():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])(string_in_body_response)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert (
        generic_checks.string_in_body(domain, string_in_body_no_match, False) == False
    )


def test_check_string_in_body_failure_on_no_body():
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body"])("")

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    assert (
        generic_checks.string_in_body(domain, string_in_body_full_match, False) == False
    )


## substrings_in_strings
def test_substrings_in_strings_for_single_string():
    assert generic_checks.substrings_in_strings("abc", "abc") == "abc"


def test_substrings_in_strings_for_single_substring():
    assert generic_checks.substrings_in_strings("b", "abc") == "abc"


def test_substrings_in_strings_for_multiple_substring():
    assert generic_checks.substrings_in_strings(["a", "b", "c"], "abc") == "abc"


def test_substrings_in_strings_returns_first_for_multiple_strings():
    assert generic_checks.substrings_in_strings("a", ["abc", "aed"]) == "abc"


def test_substrings_in_strings_no_subtrings():
    assert generic_checks.substrings_in_strings("", ["abc", "aed"]) == ""


def test_substrings_in_strings_no_strings():
    assert generic_checks.substrings_in_strings("a", "") == ""


def test_substrings_in_strings_nothing():
    assert generic_checks.substrings_in_strings("", "") == ""


## string_in_cname
def test_string_in_cname_for_single_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert generic_checks.string_in_cname(domain, "abc") == True


def test_string_in_cname_for_single_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert generic_checks.string_in_cname(domain, "b") == True


def test_string_in_cname_where_cname_is_subtring_of_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert generic_checks.string_in_cname(domain, "abcd") == False


def test_string_in_cname_for_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert generic_checks.string_in_cname(domain, ["abc", "def"]) == True


def test_string_in_cname_for_one_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "hij"]
    assert generic_checks.string_in_cname(domain, ["abc", "def"]) == True


def test_string_in_cname_for_one_of_multiple_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "hij"]
    assert generic_checks.string_in_cname(domain, ["def", "h"]) == True


def test_string_in_cname_for_none_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert generic_checks.string_in_cname(domain, ["hij", "klm"]) == False


def test_string_in_cname_for_none_matching_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert generic_checks.string_in_cname(domain, "hij") == False


def test_string_in_cname_with_no_CNAME_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = []
    assert generic_checks.string_in_cname(domain, "abc") == False


def test_string_in_cname_multiple_with_no_CNAME_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = []
    assert generic_checks.string_in_cname(domain, ["abc", "def"]) == False


## string_in_ns
def test_string_in_ns_for_single_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert generic_checks.string_in_ns(domain, "abc") == True


def test_string_in_ns_for_single_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert generic_checks.string_in_ns(domain, "b") == True


def test_string_in_ns_where_ns_is_subtring_of_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert generic_checks.string_in_ns(domain, "abcd") == False


def test_string_in_ns_for_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert generic_checks.string_in_ns(domain, ["abc", "def"]) == True


def test_string_in_ns_for_one_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "hij"]
    assert generic_checks.string_in_ns(domain, ["abc", "def"]) == True


def test_string_in_ns_for_one_of_multiple_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "hij"]
    assert generic_checks.string_in_ns(domain, ["def", "h"]) == True


def test_string_in_ns_for_none_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert generic_checks.string_in_ns(domain, ["hij", "klm"]) == False


def test_string_in_ns_for_none_matching_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["abc", "def"]
    assert generic_checks.string_in_ns(domain, "hij") == False


def test_string_in_ns_with_no_ns_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = []
    assert generic_checks.string_in_ns(domain, "abc") == False


def test_string_in_ns_multiple_with_no_ns_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = []
    assert generic_checks.string_in_ns(domain, ["abc", "def"]) == False


## ipv4_in_A
def test_ipv4_in_A_for_single_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "2.2.2.2"]
    assert generic_checks.ipv4_in_A(domain, "1.1.1.1") == True


def test_ipv4_in_A_for_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "2.2.2.2"]
    assert generic_checks.ipv4_in_A(domain, ["1.1.1.1", "2.2.2.2"]) == True


def test_ipv4_in_A_for_one_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "3.3.3.3"]
    assert generic_checks.ipv4_in_A(domain, ["1.1.1.1", "2.2.2.2"]) == True


def test_ipv4_in_A_for_none_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "2.2.2.2"]
    assert generic_checks.ipv4_in_A(domain, ["3.3.3.3", "4.4.4.4"]) == False


def test_ipv4_in_A_for_none_matching_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "2.2.2.2"]
    assert generic_checks.ipv4_in_A(domain, "3.3.3.3") == False


def test_ipv4_in_A_with_no_A_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    assert generic_checks.ipv4_in_A(domain, "1.1.1.1") == False


def test_ipv4_in_A_multiple_with_no_A_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    assert generic_checks.ipv4_in_A(domain, ["1.1.1.1", "2.2.2.2"]) == False


## ipv6_in_AAAA
def test_ipv6_in_AAAA_for_single_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert generic_checks.ipv6_in_AAAA(domain, "::1") == True


def test_ipv6_in_AAAA_for_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert generic_checks.ipv6_in_AAAA(domain, ["::1", "::2"]) == True


def test_ipv6_in_AAAA_for_one_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::3"]
    assert generic_checks.ipv6_in_AAAA(domain, ["::1", "::2"]) == True


def test_ipv6_in_AAAA_for_none_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert generic_checks.ipv6_in_AAAA(domain, ["::3", "::4"]) == False


def test_ipv6_in_AAAA_for_none_matching_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert generic_checks.ipv6_in_AAAA(domain, "::3") == False


def test_ipv6_in_AAAA_with_no_AAAA_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = []
    assert generic_checks.ipv6_in_AAAA(domain, "::1") == False


def test_ipv6_in_AAAA_multiple_with_no_AAAA_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = []
    assert generic_checks.ipv6_in_AAAA(domain, ["::1", "::2"]) == False


## no_SOA_on_NS


def test_no_SOA_on_NS_with_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch("domain.Domain.SOA", return_value=[], new_callable=PropertyMock):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert generic_checks.no_SOA_on_NS(domain) == True


def test_no_SOA_on_NS_with_no_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch(
        "domain.Domain.SOA", return_value=["SOA RECORD HERE"], new_callable=PropertyMock
    ):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert generic_checks.no_SOA_on_NS(domain) == False


def test_no_SOA_on_NS_with_no_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = []
    assert generic_checks.no_SOA_on_NS(domain) == False

from domain import Domain
from signatures.generic import CNAME
from unittest.mock import patch, PropertyMock


def test_match_for_single_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, "abc") == True


def test_match_for_single_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, "b") == True


def test_match_where_cname_is_subtring_of_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, "abcd") == False


def test_match_for_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, ["abc", "def"]) == True


def test_match_for_one_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "hij"]
    assert CNAME.match(domain, ["abc", "def"]) == True


def test_match_for_one_of_multiple_substring():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "hij"]
    assert CNAME.match(domain, ["def", "h"]) == True


def test_match_for_none_of_multiple_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, ["hij", "klm"]) == False


def test_match_for_none_matching_string():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["abc", "def"]
    assert CNAME.match(domain, "hij") == False


def test_match_with_no_CNAME_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = []
    assert CNAME.match(domain, "abc") == False


def test_match_multiple_with_no_CNAME_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = []
    assert CNAME.match(domain, ["abc", "def"]) == False


## NX_DOMAIN_on_resolve

domain_with_cname = Domain("mock.local", fetch_standard_records=False)
domain_with_cname.CNAME = ["cname"]


def test_NX_DOMAIN_on_resolve_success():
    with patch("domain.Domain.query", return_value=[]):
        assert CNAME.NX_DOMAIN_on_resolve(domain_with_cname) == True


def test_NX_DOMAIN_on_resolve_failure_A_record_found():
    def query(self, type):
        return "something" if type == "A" else []

    with patch("domain.Domain.query", new=query):
        assert CNAME.NX_DOMAIN_on_resolve(domain_with_cname) == False


def test_NX_DOMAIN_on_resolve_failure_AAAA_record_found():
    def query(self, type):
        return "something" if type == "AAAA" else []

    with patch("domain.Domain.query", new=query):
        assert CNAME.NX_DOMAIN_on_resolve(domain_with_cname) == False


def test_NX_DOMAIN_on_resolve_failure_CNAME_record_found():
    def query(self, type):
        return "something" if type == "CNAME" else []

    with patch("domain.Domain.query", new=query):
        assert CNAME.NX_DOMAIN_on_resolve(domain_with_cname) == False


def test_NX_DOMAIN_on_resolve_failure_NS_record_found():
    def query(self, type):
        return "something" if type == "NS" else []

    with patch("domain.Domain.query", new=query):
        assert CNAME.NX_DOMAIN_on_resolve(domain_with_cname) == False


def test_NX_DOMAIN_on_resolve_failure_no_cname():
    domain = Domain("mock.local", fetch_standard_records=False)
    with patch("domain.Domain.query", return_value=["something"]):
        assert CNAME.NX_DOMAIN_on_resolve(domain_with_cname) == False

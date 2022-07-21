from domain import Domain
from signatures.generic import CNAME


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

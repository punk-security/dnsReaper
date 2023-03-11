from signatures.checks import helpers


## substrings_in_strings
def test_substrings_in_strings_for_single_string():
    assert helpers.substrings_in_strings("abc", "abc") == "abc"


def test_substrings_in_strings_for_single_substring():
    assert helpers.substrings_in_strings("b", "abc") == "abc"


def test_substrings_in_strings_for_multiple_substring():
    assert helpers.substrings_in_strings(["a", "b", "c"], "abc") == "abc"


def test_substrings_in_strings_returns_first_for_multiple_strings():
    assert helpers.substrings_in_strings("a", ["abc", "aed"]) == "abc"


def test_substrings_in_strings_no_subtrings():
    assert helpers.substrings_in_strings("", ["abc", "aed"]) == ""


def test_substrings_in_strings_no_strings():
    assert helpers.substrings_in_strings("a", "") == ""


def test_substrings_in_strings_nothing():
    assert helpers.substrings_in_strings("", "") == ""

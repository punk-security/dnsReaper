from domain import Domain
from signatures.checks import A


def test_match_for_single_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "2.2.2.2"]
    assert A.match(domain, "1.1.1.1") == True


def test_match_for_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "2.2.2.2"]
    assert A.match(domain, ["1.1.1.1", "2.2.2.2"]) == True


def test_match_for_one_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "3.3.3.3"]
    assert A.match(domain, ["1.1.1.1", "2.2.2.2"]) == True


def test_match_for_none_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "2.2.2.2"]
    assert A.match(domain, ["3.3.3.3", "4.4.4.4"]) == False


def test_match_for_none_matching_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1", "2.2.2.2"]
    assert A.match(domain, "3.3.3.3") == False


def test_match_with_no_A_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    assert A.match(domain, "1.1.1.1") == False


def test_match_multiple_with_no_A_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    assert A.match(domain, ["1.1.1.1", "2.2.2.2"]) == False

from domain import Domain
import signatures.generic


def test_ipv6_in_AAAA_for_single_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert signatures.generic.AAAA.match(domain, "::1") == True


def test_ipv6_in_AAAA_for_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert signatures.generic.AAAA.match(domain, ["::1", "::2"]) == True


def test_ipv6_in_AAAA_for_one_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::3"]
    assert signatures.generic.AAAA.match(domain, ["::1", "::2"]) == True


def test_ipv6_in_AAAA_for_none_of_multiple_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert signatures.generic.AAAA.match(domain, ["::3", "::4"]) == False


def test_ipv6_in_AAAA_for_none_matching_ip():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = ["::1", "::2"]
    assert signatures.generic.AAAA.match(domain, "::3") == False


def test_ipv6_in_AAAA_with_no_AAAA_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = []
    assert signatures.generic.AAAA.match(domain, "::1") == False


def test_ipv6_in_AAAA_multiple_with_no_AAAA_records():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.AAAA = []
    assert signatures.generic.AAAA.match(domain, ["::1", "::2"]) == False

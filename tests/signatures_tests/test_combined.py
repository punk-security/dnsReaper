from domain import Domain
import combined_checks

## matching_ipv4_or_ipv6
def test_matching_ipv4_or_ipv6_ipv4_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1"]
    domain.AAAA = []
    assert combined_checks.matching_ipv4_or_ipv6(domain, "1.1.1.1", "::1") == True


def test_matching_ipv4_or_ipv6_ipv6_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.AAAA = ["::1"]
    assert combined_checks.matching_ipv4_or_ipv6(domain, "1.1.1.1", "::1") == True


def test_matching_ipv4_or_ipv6_no_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.AAAA = []
    assert combined_checks.matching_ipv4_or_ipv6(domain, "1.1.1.1", "::1") == False


## macthing_ipv4_or_cname
def test_matching_ipv4_or_cname_ipv4_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = ["1.1.1.1"]
    domain.CNAME = []
    assert combined_checks.matching_ipv4_or_cname(domain, "1.1.1.1", "goose") == True


def test_matching_ipv4_or_cname_cname_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.CNAME = ["goose"]
    assert combined_checks.matching_ipv4_or_cname(domain, "1.1.1.1", "goose") == True


def test_matching_ipv4_or_cname_no_match():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.A = []
    domain.AAAA = []
    assert combined_checks.matching_ipv4_or_cname(domain, "1.1.1.1", "goose") == False
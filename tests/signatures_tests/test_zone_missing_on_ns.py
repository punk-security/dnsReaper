from domain import Domain
from signatures import zone_missing_on_ns


def test_potential_success_with_a_nameserver():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    assert zone_missing_on_ns.test.potential(domain) == True


def test_potential_success_with_multiple_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns1", "ns2"]
    assert zone_missing_on_ns.test.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert zone_missing_on_ns.test.potential(domain) == False

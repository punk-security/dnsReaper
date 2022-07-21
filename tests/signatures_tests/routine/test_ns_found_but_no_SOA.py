from domain import Domain
from signatures.routine.ns_found_but_no_SOA import (
    ns_found_but_no_SOA,
)

test = ns_found_but_no_SOA("ns1", "INFO")


def test_potential_success_with_matching_nameserver():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns1"]
    assert test.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert test.potential(domain) == False

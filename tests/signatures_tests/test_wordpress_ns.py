from domain import Domain
from signatures import wordpress_com_ns


def test_potential_success_with_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    for ns in wordpress_com_ns.wordpress_ns:
        domain.NS = [ns]
    assert wordpress_com_ns.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert wordpress_com_ns.potential(domain) == False

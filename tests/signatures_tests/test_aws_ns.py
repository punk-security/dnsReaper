from domain import Domain
from signatures import aws_ns


def test_potential_success_with_matching_nameserver():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns-687.awsdns-21.net"]
    assert aws_ns.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert aws_ns.potential(domain) == False

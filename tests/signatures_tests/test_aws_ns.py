from domain import Domain
from signatures import aws_ns


def test_check_ACTIVE():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns-40.awsdns-05.com"]
    assert aws_ns.test.check(domain) == True

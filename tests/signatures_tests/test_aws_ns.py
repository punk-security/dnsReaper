from domain import Domain
from signatures import aws_ns

from unittest.mock import patch, PropertyMock


def test_potential_success_with_matching_nameserver():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns-687.awsdns-21.net"]
    assert aws_ns.potential(domain) == True


def test_potential_success_with_matching_nameserver_second():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns1.google.com", "ns-687.awsdns-21.net"]
    assert aws_ns.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns1.google.com"]
    assert aws_ns.potential(domain) == False


def test_potential_failure_on_no_NS():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert aws_ns.potential(domain) == False


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch("domain.Domain.SOA", return_value=[]):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert aws_ns.check(domain) == True


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch("domain.Domain.SOA", return_value=[], new_callable=PropertyMock):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert aws_ns.check(domain) == True


def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch(
        "domain.Domain.SOA", return_value=["SOA RECORD HERE"], new_callable=PropertyMock
    ):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert aws_ns.check(domain) == False

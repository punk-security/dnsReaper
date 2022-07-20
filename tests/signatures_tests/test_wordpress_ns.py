from domain import Domain
from signatures import wordpress_com_ns

import mocks
from unittest.mock import patch, PropertyMock


def test_potential_success_with_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    for ns in wordpress_com_ns.wordpress_ns:
        domain.NS = [ns]
    assert wordpress_com_ns.potential(domain) == True


def test_potential_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert wordpress_com_ns.potential(domain) == False


def test_check_success():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch("domain.Domain.SOA", return_value=[], new_callable=PropertyMock):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert wordpress_com_ns.check(domain) == True


def test_check_failure():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns"]
    with patch(
        "domain.Domain.SOA", return_value=["SOA RECORD HERE"], new_callable=PropertyMock
    ):
        with patch("domain.Domain.query", return_value=["10.10.10.10"]):
            assert wordpress_com_ns.check(domain) == False

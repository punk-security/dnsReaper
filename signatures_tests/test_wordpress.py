from domain import Domain
from signatures import wordpress_com

from collections import namedtuple


def test_potential_success_with_matching_nameservers():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = wordpress_com.wordpress_ns
    assert wordpress_com.potential(domain) == True


def test_potential_success_with_matching_nameserver():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = [wordpress_com.wordpress_ns[0]]
    assert wordpress_com.potential(domain) == True


def test_potential_success_with_matching_nameserver_second():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns1.google.com", wordpress_com.wordpress_ns[0]]
    assert wordpress_com.potential(domain) == True


def test_potential_success_with_matching_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["goose.wordpress.com"]
    assert wordpress_com.potential(domain) == True


def test_potential_failure_on_no_matching_nameserver():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.NS = ["ns1.google.com"]
    assert wordpress_com.potential(domain) == False


def test_potential_faliure_with_matching_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    domain.CNAME = ["goose.com"]
    assert wordpress_com.potential(domain) == False


def test_potential_failure_on_no_NS_and_CNAME():
    domain = Domain("mock.local", fetch_standard_records=False)
    assert wordpress_com.potential(domain) == False

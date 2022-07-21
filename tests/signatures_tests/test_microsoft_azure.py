from domain import Domain
from signatures import microsoft_azure


def test_check_success_ACTIVE():
    for cname in microsoft_azure.test.cname:
        domain = Domain("mock.local", fetch_standard_records=False)
        domain.CNAME = [f"sdfsdfsdfsdas{cname}"]
        print(f"Testing CNAME '{domain.CNAME[0]}'")
        assert microsoft_azure.test.check(domain) == True

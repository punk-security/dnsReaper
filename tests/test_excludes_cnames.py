import pytest
from argparse import Namespace
from scan import scan_domain
from unittest.mock import MagicMock

# Mock domain with proper record structure
class MockDomain:
    def __init__(self, name, cname):
        self.domain = name
        self.records = []
        self.A = ["127.0.0.1"]
        self.AAAA = ["::1"]
        self.NS = ["ns1.example.com"]
        self.should_fetch_std_records = False
        
        # Add CNAME record(s)
        if isinstance(cname, list):
            for cn in cname:
                self.records.append(MagicMock(type='CNAME', value=cn))
        else:
            self.records.append(MagicMock(type='CNAME', value=cname))

    async def fetch_std_records(self):
        pass

    async def fetch_external_records(self):
        pass

# Fixed signature with proper CONFIDENCE enum
class DummySignature:
    __name__ = "DummySignature"
    
    class test:
        class CONFIDENCE:
            name = "HIGH"
            value = "HIGH"
        
        INFO = "dummy info"
        more_info_url = "http://example.com"
        
        @staticmethod
        def potential(domain):
            return True
        
        @staticmethod
        async def check(domain):
            return True

# Output handler
class DummyOutput:
    def write(self, finding):
        pass

@pytest.mark.asyncio
async def test_single_cname_excluded():
    findings = []
    domain = MockDomain("a.punksecurity.co.uk", "b.punksecurity.io")
    args = Namespace(excluded_cnames=["b.punksecurity.io"])
    
    await scan_domain(domain, [DummySignature()], findings, DummyOutput(), args)
    assert len(findings) == 0

@pytest.mark.asyncio
async def test_multiple_cnames_excluded():
    findings = []
    domain = MockDomain("test.com", "c.punksecurity.io")
    args = Namespace(excluded_cnames=["b.punksecurity.io", "c.punksecurity.io"])
    
    await scan_domain(domain, [DummySignature()], findings, DummyOutput(), args)
    assert len(findings) == 0

@pytest.mark.asyncio
async def test_mixed_case_cname_excluded():
    findings = []
    domain = MockDomain("test.com", "MiXeD.CaSe.IO")
    args = Namespace(excluded_cnames=["mixed.case.io"])
    
    await scan_domain(domain, [DummySignature()], findings, DummyOutput(), args)
    assert len(findings) == 0


@pytest.mark.asyncio
async def test_multiple_cnames_one_excluded():
    findings = []
    domain = MockDomain("test.com", ["safe.example.com", "risky.example.com"])
    args = Namespace(excluded_cnames=["safe.example.com"])
    
    await scan_domain(domain, [DummySignature()], findings, DummyOutput(), args)
    assert len(findings) == 0
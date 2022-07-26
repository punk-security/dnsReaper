from collections import namedtuple
import dns.resolver
from functools import lru_cache

import requests
import logging

import urllib3


class Domain:
    @property
    @lru_cache
    def SOA(self):
        return self.query("SOA")

    @property
    @lru_cache
    def NX_DOMAIN(self):
        record_types = ["A", "AAAA", "CNAME", "TXT", "MX", "NS"]
        for record_type in record_types:
            if self.query(record_type):
                return False
        return True

    def query(self, type):
        try:
            resp = self.resolver.resolve(self.domain, type)
            return [record.to_text().rstrip(".") for record in resp]
        except:
            return []

    def fetch_std_records(self):
        self.CNAME = self.query("CNAME")
        self.A = self.query("A")
        self.AAAA = self.query("AAAA")
        if self.CNAME:
            # return early if we get a CNAME otherwise we get records for the cname aswell
            # this is actually desirable for A/AAAA but not NS as the next zone
            # will be queried based on the CNAME value, not the original domain
            return
        self.NS = self.query("NS")

    def __init__(self, domain, fetch_standard_records=True, ns=None):
        self.domain = domain.rstrip(".")
        self.NS = []
        self.A = []
        self.AAAA = []
        self.CNAME = []
        self.requests = requests
        if ns == None:
            self.resolver = dns.resolver
        else:
            self.resolver = dns.resolver.Resolver()
            self.resolver.nameservers = [ns]
        if fetch_standard_records:
            self.fetch_std_records()

    @lru_cache
    def fetch_web(self, uri="", https=True, params={}):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        protocol = "https" if https else "http"
        url = f"{protocol}://{self.domain}/{uri}"
        try:
            resp = self.requests.get(url, timeout=5, verify=False, params=params)
            web_status = resp.status_code
            web_body = resp.content.decode()
        except:
            web_status = 0
            web_body = ""
        return namedtuple("web_response", ["status_code", "body"])(web_status, web_body)

    def __repr__(self):
        return self.domain

    @property
    def records(self):
        return f"""
        A: {self.A}
        AAAA: {self.AAAA}
        CNAME: {self.CNAME}
        NS: {self.NS}
        """

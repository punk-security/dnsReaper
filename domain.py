from collections import namedtuple
import dns.resolver
from functools import lru_cache

import requests
import logging


class Domain:
    @property
    @lru_cache
    def SOA(self):
        return self.query("SOA")

    def query(self, type):
        try:
            resp = self.resolver.resolve(self.domain, type)
            return [record.to_text() for record in resp]
        except:
            return []

    def fetch_std_records(self):
        self.NS = self.query("NS")
        self.A = self.query("A")
        self.AAAA = self.query("AAAA")
        self.CNAME = self.query("CNAME")

    def __init__(self, domain, fetch_standard_records=True, ns=None):
        self.domain = domain
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

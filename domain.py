import ipaddress
import socket
from collections import namedtuple
import dns.asyncresolver
from functools import lru_cache

import logging

import urllib3

import collections

collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
import whois

import aiohttp


class Domain:
    resolver = None

    @property
    # @lru_cache
    async def SOA(self):
        return await self.query("SOA")

    @property
    # @lru_cache
    async def NX_DOMAIN(self):
        record_types = ["A", "AAAA", "CNAME", "TXT", "MX", "NS"]
        for record_type in record_types:
            if await self.query(record_type):
                return False
        return True

    async def query(self, type):
        try:
            resp = await self.resolver.resolve(self.domain, type)
            return [record.to_text().rstrip(".") for record in resp]
        except:
            return []

    async def fetch_std_records(self):
        # TODO: is this recursive?
        self.CNAME = await self.query("CNAME")
        self.A = await self.query("A")
        self.AAAA = await self.query("AAAA")
        if self.CNAME or self.A or self.AAAA:
            # return early if we get a CNAME otherwise we get records for the cname aswell
            # this is actually desirable for A/AAAA but not NS as the next zone
            # will be queried based on the CNAME value, not the original domain
            return
        self.NS = await self.query("NS")

    async def fetch_external_records(self):
        for cname in self.CNAME:
            split_cname = cname.split(".", 1)
            if len(split_cname) == 1:
                continue  # This cname has no zone to assess
            if self.base_domain == split_cname[1]:
                continue  # Same zone, dont fetch
            d = Domain(cname)
            await d.fetch_std_records()
            self.A += d.A
            self.AAAA += d.AAAA
            self.CNAME += d.CNAME
        for ns in self.NS:
            try:
                d = Domain(self.domain)
                d.ns = ns
                await d.set_NS()
                self.A += d.A
                self.AAAA += d.AAAA
            except:
                logging.debug(
                    f"We could not resolve the provided NS record '{ns}' to an ip"
                )

    async def set_NS(self):
        if self.ns == None:
            self.resolver = dns.asyncresolver
        else:
            if type(self.ns) != str:
                logging.error(f"Cannot set custom NS as {ns} not a string")
            self.resolver = dns.asyncresolver.Resolver()

            try:
                ipaddress.ip_address(self.ns)
                self.resolver.nameservers = [self.ns]
            except ValueError:
                try:
                    nameservers = list(
                        map(
                            lambda rr: rr.address,
                            (await self.resolver.resolve(self.ns.rstrip("."))).rrset,
                        )
                    )
                    self.resolver.nameservers = nameservers
                except:
                    self.resolver.nameservers = []
        self.resolver.timeout = 1

    def set_custom_NS_sync(self, ns: str):
        if type(ns) != str:
            logging.error(f"Cannot set custom NS as {ns} not a string")
        self.resolver = dns.asyncresolver.Resolver()

        try:
            ipaddress.ip_address(ns)
            self.resolver.nameservers = [ns]
        except ValueError:
            try:
                self.resolver.nameservers = [socket.gethostbyname(ns.rstrip("."))]
            except:
                self.resolver.nameservers = []

    def set_base_domain(self):
        split_domain = self.domain.split(".", 1)
        if len(split_domain) > 1:
            self.base_domain = split_domain[1]
        else:
            self.base_domain = "."

    def __init__(self, domain, fetch_standard_records=True):
        self.domain = domain.rstrip(".")
        self.NS = []
        self.A = []
        self.AAAA = []
        self.CNAME = []
        self.set_base_domain()
        self.should_fetch_std_records = fetch_standard_records

    # @lru_cache
    async def fetch_web(self, uri="", https=True, params={}):
        protocol = "https" if https else "http"
        url = f"{protocol}://{self.domain}/{uri}"
        try:
            # resp = self.requests.get(url, timeout=5, verify=False, params=params)
            async with aiohttp.ClientSession() as session:
                resp = await session.get(url, ssl=False)
                web_status = resp.status
                web_body = await resp.text()
        except:
            web_status = 0
            web_body = ""
        return namedtuple("web_response", ["status_code", "body"])(web_status, web_body)

    @property
    @lru_cache
    def is_registered(self):
        try:
            whois.whois(self.domain)
            return True
        except whois.parser.PywhoisError as e:
            if e.args[0] == "No whois server is known for this kind of object.":
                # This is the only case of a potentially registered domain
                # triggering a PywhoisError
                # https://github.com/richardpenman/whois/blob/56dc7e41d134e6d4343ad80a48533681bd887ff2/whois/parser.py#L201
                return True
            return False
        except Exception:
            return True

    def __repr__(self):
        return self.domain

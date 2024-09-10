import ipaddress
from collections import namedtuple
from typing import Optional

import dns.asyncresolver

import logging
import collections

collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping

import asyncwhois
import aiohttp
import ssl

from resolver import Resolver


class Domain:
    resolver = Resolver()

    @property
    async def SOA(self):
        return await self.query("SOA")

    @property
    async def NX_DOMAIN(self):
        return (await self.resolver.resolve(self.domain, "A"))["NX_DOMAIN"]

    async def query(self, type):
        try:
            resp = await self.resolver.resolve(self.domain, type)
            return resp[type]
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
                await d.set_resolver_nameserver(ns)
                self.A += d.A
                self.AAAA += d.AAAA
            except:
                logging.debug(
                    f"We could not resolve the provided NS record '{ns}' to an ip"
                )

    async def set_resolver_nameserver(self, ns: Optional[str] = None):
        if ns is None:
            self.resolver = dns.asyncresolver
            self.resolver.timeout = 1

            return

        if type(ns) != str:
            logging.error(f"Cannot set custom NS as {ns} not a string")

            raise RuntimeError(f"Invalid NS type - expected str got {type(ns)}")

        self.resolver = dns.asyncresolver.Resolver()
        self.resolver.timeout = 1

        try:
            ipaddress.ip_address(ns)
            self.resolver.nameservers = [ns]
            return
        except ValueError:
            # if ns isn't a valid IP address, attempt to resolve it
            try:
                nameservers = list(
                    map(
                        lambda rr: rr.address,
                        (await self.resolver.resolve(ns.rstrip("."))).rrset,
                    )
                )
                self.resolver.nameservers = nameservers
            except:
                # TODO: document why this gets set to an empty list
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
        self.base_domain = None

    def get_session(self):
        return aiohttp.ClientSession()

    async def fetch_web(self, uri="", https=True):
        protocol = "https" if https else "http"
        url = f"{protocol}://{self.domain}/{uri}"

        # We must disable SSL validation because vulnerable domains probably won't have a valid cert on the other end
        # e.g. github
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        try:
            async with self.get_session() as session:
                resp = await session.get(url, ssl=ssl_context, headers=headers)
                web_status = resp.status
                web_body = await resp.text()
        except:
            web_status = 0
            web_body = ""
        return namedtuple("web_response", ["status_code", "body"])(web_status, web_body)

    @property
    async def is_registered(self):
        try:
            await asyncwhois.aio_whois(self.domain)
            return True
        except asyncwhois.NotFoundError:
            return False
        except Exception:
            return True

    def __repr__(self):
        return self.domain

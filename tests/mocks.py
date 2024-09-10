from collections import namedtuple
import socket
from domain import Domain
import requests
import dns.resolver
import ipaddress
from uuid import uuid4

import aiohttp


def random_string():
    return f"a{uuid4().hex[:8]}"


def mock_web_response_with_static_value(
    domain: Domain, body: str = "", status_code: int = 0
) -> Domain:
    async def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body", "status_code"])(body, status_code)

    domain.fetch_web = mock_fetch_web


def mock_web_request_by_providing_static_host_resolution(
    domain: Domain, hostname: str
) -> Domain:
    requests_adapter = HostHeaderAdapter()
    requests_adapter.set_static_host_resolution(hostname)
    patched_requests = requests.session()
    patched_requests.mount("https://", requests_adapter)
    patched_requests.mount("http://", requests_adapter)
    domain.requests = patched_requests


def mock_web_request_by_providing_custom_ns(domain: Domain, ns: str) -> Domain:
    requests_adapter = HostHeaderAdapter()
    requests_adapter.set_ns_for_resolution(ns)
    patched_requests = requests.session()
    patched_requests.mount("https://", requests_adapter)
    patched_requests.mount("http://", requests_adapter)
    domain.requests = patched_requests


class HostHeaderAdapter(requests.adapters.HTTPAdapter):
    def set_static_host_resolution(self, host):
        self.host = self.resolve_to_ip(host)

    def set_ns_for_resolution(self, ns):
        self.ns = self.resolve_to_ip(ns)

    def resolve_via_ns(self, domain):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [self.ns]
        response = resolver.resolve(domain)
        return [record.to_text() for record in response][0]

    def resolve_to_ip(self, name):
        try:
            # return the name if its already an ip
            ipaddress.ip_address(name)
            return name
        except:
            response = dns.resolver.resolve(name)
            ip = [record.to_text() for record in response][0]
            return self.resolve_to_ip(ip)

    def wrap_if_ipv6(self, ip):
        if ip.count(":") > 1:
            return f"[{ip}]"
        return ip

    def send(self, request, **kwargs):
        from urllib.parse import urlparse

        connection_pool_kwargs = self.poolmanager.connection_pool_kw
        result = urlparse(request.url)
        try:
            # Try use a static ip
            resolved_ip = self.host
        except:
            # If that fails, try and resolve
            resolved_ip = self.resolve_to_ip(result.hostname)

        resolved_ip = self.wrap_if_ipv6(resolved_ip)

        request.url = request.url.replace(
            "//" + result.hostname,
            "//" + resolved_ip,
        )
        if "https" in request.url:
            connection_pool_kwargs["server_hostname"] = result.hostname  # SNI
            connection_pool_kwargs["assert_hostname"] = result.hostname

        # overwrite the host header
        request.headers["Host"] = result.hostname
        return super(HostHeaderAdapter, self).send(request, **kwargs)


class CustomResolver:
    def __init__(self, ip):
        self.ip = ip

    async def resolve(self, host, port=0, family=socket.AF_INET):
        return [
            {
                "hostname": host,
                "host": self.ip,
                "port": port,
                "family": family,
                "proto": socket.IPPROTO_TCP,
                "flags": 0,
            }
        ]


def generate_mock_aiohttp_session_with_forced_ip_resolution(ip):
    def mock_aiohttp_session_with_forced_resolution():
        resolver = CustomResolver(ip)
        conn = aiohttp.TCPConnector(resolver=resolver)
        return aiohttp.ClientSession(connector=conn)

    return mock_aiohttp_session_with_forced_resolution


def generate_mock_aiohttp_session_with_forced_cname_resolution(cname):
    ip = [record.to_text() for record in dns.resolver.resolve(cname)][0]

    def mock_aiohttp_session_with_forced_resolution():
        resolver = CustomResolver(ip)
        conn = aiohttp.TCPConnector(resolver=resolver)
        return aiohttp.ClientSession(connector=conn)

    return mock_aiohttp_session_with_forced_resolution

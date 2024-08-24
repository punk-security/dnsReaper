import dns.asyncresolver
import asyncio
import random
import time
import os

import dns.resolver

import socket
import struct

import logging

# DNS query types
TYPE_A = 1
TYPE_NS = 2
TYPE_CNAME = 5
TYPE_SOA = 6
TYPE_AAAA = 28
TYPE_MX = 15

QUERY_TYPES = {
    "A": TYPE_A,
    "NS": TYPE_NS,
    "CNAME": TYPE_CNAME,
    "SOA": TYPE_SOA,
    "AAAA": TYPE_AAAA,
    "MX": TYPE_MX,
}


class DNSException(Exception):
    pass


class NXDomainException(DNSException):
    pass


class NoAnswerException(DNSException):
    pass


def build_dns_query(domain, qtype):
    # Transaction ID
    transaction_id = 0x1234

    # Flags: standard query with recursion
    flags = 0x0100

    # Questions
    questions = 1

    # Answer RRs
    answer_rrs = 0

    # Authority RRs
    authority_rrs = 0

    # Additional RRs
    additional_rrs = 0

    # Header
    header = struct.pack(
        ">HHHHHH",
        transaction_id,
        flags,
        questions,
        answer_rrs,
        authority_rrs,
        additional_rrs,
    )

    # Question
    question = b""
    for part in domain.split("."):
        question += struct.pack("B", len(part)) + part.encode()

    question += struct.pack("B", 0)  # End of the domain name

    # Type and Class
    question += struct.pack(">HH", qtype, 1)  # QTYPE = qtype, QCLASS = IN

    return header + question


def parse_dns_response(response):
    def decode_name(offset):
        labels = []
        while True:
            length = response[offset]
            if length & 0xC0 == 0xC0:
                pointer = struct.unpack_from("!H", response, offset)[0]
                pointer &= 0x3FFF
                labels.append(decode_name(pointer)[0])
                offset += 2
                break
            elif length == 0:
                offset += 1
                break
            else:
                offset += 1
                labels.append(response[offset : offset + length].decode())
                offset += length
        return ".".join(labels), offset

    header = struct.unpack(">HHHHHH", response[:12])
    rcode = header[1] & 0x000F  # Response code
    question_count = header[2]
    answer_count = header[3]

    if rcode == 3:  # NXDOMAIN
        raise NXDomainException("The domain does not exist (NXDOMAIN)")

    if answer_count == 0:
        raise NoAnswerException("No answer found in the DNS response")

    offset = 12
    for _ in range(question_count):
        while response[offset] != 0:
            offset += response[offset] + 1
        offset += 5  # null byte + QTYPE + QCLASS

    records = {
        "A": [],
        "NS": [],
        "CNAME": [],
        "SOA": [],
        "AAAA": [],
        "MX": [],
        "NX_DOMAIN": False,
    }

    for _ in range(answer_count):
        name, offset = decode_name(offset)
        rtype, rclass, ttl, data_length = struct.unpack_from(">HHIH", response, offset)
        offset += 10

        if rtype == TYPE_A:
            ip = socket.inet_ntoa(response[offset : offset + data_length])
            records["A"].append(ip)
        elif rtype == TYPE_NS:
            ns, _ = decode_name(offset)
            records["NS"].append(ns)
        elif rtype == TYPE_CNAME:
            cname, _ = decode_name(offset)
            records["CNAME"].append(cname)
        elif rtype == TYPE_SOA:
            mname, offset = decode_name(offset)
            rname, offset = decode_name(offset)
            serial, refresh, retry, expire, minimum = struct.unpack_from(
                ">IIIII", response, offset
            )
            soa = {
                "mname": mname,
                "rname": rname,
                "serial": serial,
                "refresh": refresh,
                "retry": retry,
                "expire": expire,
                "minimum": minimum,
            }
            records["SOA"].append(soa)
            offset += 20
        elif rtype == TYPE_AAAA:
            ip = socket.inet_ntop(
                socket.AF_INET6, response[offset : offset + data_length]
            )
            records["AAAA"].append(ip)
        elif rtype == TYPE_MX:
            preference = struct.unpack_from(">H", response, offset)[0]
            offset += 2
            exchange, _ = decode_name(offset)
            records["MX"].append((preference, exchange))

        offset += data_length

    return records


class DnsClientProtocol(asyncio.DatagramProtocol):
    def __init__(self, query, future):
        self.query = query
        self.future = future
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.query)

    def datagram_received(self, data, addr):
        if not self.future.done():
            self.future.set_result(data)
        self.transport.close()

    def error_received(self, exc):
        if not self.future.done():
            self.future.set_exception(exc)
        self.transport.close()

    def connection_lost(self, exc):
        if not self.future.done():
            self.future.set_exception(exc)


async def resolve_dns(domain, qtype, server="8.8.8.8", port=53):
    query = build_dns_query(domain, qtype)
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: DnsClientProtocol(query, future), remote_addr=(server, port)
    )

    try:
        response = await asyncio.wait_for(future, timeout=0.5)
        records = parse_dns_response(response)
        return records
    finally:
        transport.close()


class Resolver:
    attempted_resolutions = 0
    resolutions = 0
    errors = 0
    no_records = 0
    nx_domains = 0

    def __init__(self, parallelism=200, nameservers=None):
        self.nameservers = nameservers if nameservers is not None else ["8.8.8.8"]
        self.semaphore = asyncio.Semaphore(parallelism)

    async def resolve(self, fqdn, type=None, retry=3):
        async with self.semaphore:
            if self.attempted_resolutions == 0:
                write_when_on_warn("\nDNS Resolving: (Feedback per 100 resolves)\n")
                write_when_on_warn(
                    "[ . = success, + = non-existent domain, x = error (likely rate-limiting)]\n"
                )
            self.attempted_resolutions += 1
            qtype = QUERY_TYPES[type]
            start = time.time()
            resp = {
                "A": [],
                "NS": [],
                "CNAME": [],
                "SOA": [],
                "AAAA": [],
                "MX": [],
                "NX_DOMAIN": False,
            }
            try:
                resp = await resolve_dns(fqdn, qtype, random.choice(self.nameservers))
                if self.resolutions % 100 == 99:
                    write_when_on_warn(".")
                self.resolutions += 1
            except NoAnswerException:
                if self.resolutions % 100 == 99:
                    write_when_on_warn(".")
                self.resolutions += 1
            except NXDomainException:
                if self.nx_domains % 100 == 99:
                    write_when_on_warn("+")
                self.nx_domains += 1
                resp["NX_DOMAIN"] = True
            except:
                if self.errors % 100 == 99:
                    write_when_on_warn("x")
                self.errors += 1
                if retry > 0:
                    await asyncio.sleep(0.1)
                    resp = await self.resolve(fqdn, type=type, retry=retry - 1)
            time_delta = time.time() - start
            if time_delta < 0.125:
                await asyncio.sleep(0.125 - time_delta)
            return resp

    @staticmethod
    async def resolve_with_ns(fqdn, ns, type=None):
        qtype = QUERY_TYPES[type]
        try:
            return await resolve_dns(fqdn, qtype, ns)
        except:
            return {"A": [], "NS": [], "CNAME": [], "SOA": [], "AAAA": [], "MX": []}


def write_when_on_warn(msg):
    if logging.root.level == logging.WARN:
        # Only in warning, as we need a clean output
        os.write(2, msg.encode())

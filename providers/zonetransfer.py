import logging
import socket

import dns.rdatatype as record_types
import dns.resolver
import dns.zone

from domain import Domain

description = "Scan multiple domains by fetching records via DNS zone transfer"


def convert_records_to_domains(root_domain, records):
    buf = {}

    for record in records:
        fqdn = f"{record[0]}.{root_domain}" if "@" != str(record[0]) else root_domain

        if fqdn not in buf.keys():
            buf[fqdn] = {}

        record_type = record[1].rdtype
        record_items = record[1].items

        if record_type == record_types.A:
            buf[fqdn]["A"] = [str(x) for x in record_items]
            continue

        if record_type == record_types.AAAA:
            buf[fqdn]["AAAA"] = [str(x) for x in record_items]
            continue

        if record_type == record_types.CNAME:
            buf[fqdn]["CNAME"] = [str(x) for x in record_items]
            continue

        if record_type == record_types.NS:
            buf[fqdn]["NS"] = [str(x) for x in record_items]
            continue

    for subdomain in buf.keys():

        def extract_records(desired_type):
            return [r.rstrip(".") for r in buf[subdomain][desired_type]]

        domain = Domain(subdomain.rstrip("."), fetch_standard_records=False)
        if "A" in buf[subdomain].keys():
            domain.A = extract_records("A")
        if "AAAA" in buf[subdomain].keys():
            domain.AAAA = extract_records("AAAA")
        if "CNAME" in buf[subdomain].keys():
            domain.CNAME = extract_records("CNAME")
        if "NS" in buf[subdomain].keys():
            domain.NS = extract_records("NS")

        yield domain


def fetch_domains(zonetransfer_nameserver, zonetransfer_domain, **args):  # NOSONAR
    ns_address = socket.gethostbyname(zonetransfer_nameserver)
    transfer_result = dns.query.xfr(ns_address, zonetransfer_domain)
    try:
        zone = dns.zone.from_xfr(transfer_result)
    except dns.xfr.TransferError as e:
        logging.error(
            f"ERROR: Nameserver {zonetransfer_nameserver} does not allow zone transfer: {e}"
        )

        return []

    return convert_records_to_domains(
        zonetransfer_domain, list(zone.iterate_rdatasets())
    )

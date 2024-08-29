import logging
import random
import socket

import dns.rdatatype as record_types
import dns.resolver
import dns.zone

from domain import Domain

description = "Scan multiple domains by fetching records via DNS zone transfer"


def convert_records_to_domains(root_domain, records):
    buf: dict[str, dict[str, list[str]]] = {}

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
            cna = []
            for x in record_items:
                cn = str(x)
                if cn.endswith("."):
                    cna.append(cn)
                else:
                    cna.append(f"{cn}.{root_domain}")

            buf[fqdn]["CNAME"] = cna
            continue

        if record_type == record_types.NS:
            buf[fqdn]["NS"] = [str(x) for x in record_items]
            continue

    for tries in []:#range(1, 5):
        changed = False
        recs_with_cname = [(rec, rec["CNAME"][0]) for sub, rec in buf.items() if "CNAME" in rec and len(rec["CNAME"])]
        # todo: remove this, just for testing
        random.Random().shuffle(recs_with_cname)

        for rec, cname in recs_with_cname:
            if cname[-1] != "." and cname in buf:
                rec.clear()
                rec |= buf[cname]
                changed = True

        # No more records to deal with
        if not changed:
            break

        if tries >= 6:
            raise RecursionError("Too many levels of record recursion. This usually indicates circular records.")

    unresolvable = [subdomain for subdomain, records in buf.items() if not records]
    if unresolvable:
        logging.warning(f"The following subdomains could not be resolved (circular?): {', '.join(unresolvable)}")

    for subdomain, records in buf.items():
        if not records:
            continue

        def extract_records(desired_type):
            return [r.rstrip(".") for r in buf[subdomain][desired_type]]

        domain = Domain(subdomain.rstrip("."), fetch_standard_records=False)
        if "A" in records:
            domain.A = extract_records("A")
        if "AAAA" in records:
            domain.AAAA = extract_records("AAAA")
        if "CNAME" in records:
            domain.CNAME = extract_records("CNAME")
        if "NS" in records:
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

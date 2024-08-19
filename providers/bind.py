import logging
from domain import Domain
import dns.zone, dns.rdatatype
from os import listdir
from os.path import isfile, join

description = "Read domains from a dns BIND zone file, or path to multiple"


def bind_file_to_domains(bind_zone_file):
    logging.debug(f"Reading domains from zonefile '{bind_zone_file}'")
    domains = []
    zone = dns.zone.from_file(bind_zone_file)
    root_domain = str(zone.origin).rstrip(".")
    for name, node in zone.nodes.items():
        domain = root_domain if str(name) == "@" else f"{str(name)}.{root_domain}"
        domain = Domain(domain, fetch_standard_records=False)
        for record in node.rdatasets:
            if record.rdtype == dns.rdatatype.A:
                domain.A = [str(r) for r in record.items]
            if record.rdtype == dns.rdatatype.AAAA:
                domain.AAAA = [str(r) for r in record.items]
            if record.rdtype == dns.rdatatype.CNAME:
                domain.CNAME = [str(r) for r in record.items]
            if record.rdtype == dns.rdatatype.NS and str(name) != "@":
                domain.NS = [str(r) for r in record.items]
        domains.append(domain)
        logging.info(f"Read {len(domains)} domains from zonefile '{bind_zone_file}'")
    return domains


def fetch_domains(bind_zone_file, **args):
    if isfile(bind_zone_file):
        domains = bind_file_to_domains(bind_zone_file)
        logging.warning(f"Read {len(domains)} domains from zone file")
    else:
        domains = []
        files = [
            join(bind_zone_file, f)
            for f in listdir(bind_zone_file)
            if isfile(join(bind_zone_file, f))
        ]
        for file in files:
            logging.debug("Reading file '{file}'")
            domains = [*domains, *bind_file_to_domains(file)]
        logging.warning(f"Read {len(domains)} domains from zone file dir")
    return domains

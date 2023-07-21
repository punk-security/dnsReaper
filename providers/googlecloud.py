import logging, os

from domain import Domain
from google.cloud import dns

description = "Scan multiple domains by fetching them from Google Cloud. Requires GOOGLE_APPLICATION_CREDENTIALS environment variable."


def get_records(zone):
    records = []

    try:
        records = zone.list_resource_record_sets(max_results=None, page_token=None)
    except Exception as e:
        logging.critical(f"Failed to fetch zone records. {e}")
        return []

    return list(records)


def convert_records_to_domains(records):
    buf = {}
    for record in records:
        if record.name not in buf.keys():
            buf[record.name] = {}

        buf[record.name][record.record_type] = record.rrdatas

    for subdomain in buf.keys():
        domain = Domain(subdomain.rstrip("."), fetch_standard_records=False)
        if "A" in buf[subdomain].keys():
            domain.A = [r.rstrip(".") for r in buf[subdomain]["A"]]
        if "AAAA" in buf[subdomain].keys():
            domain.AAAA = [r.rstrip(".") for r in buf[subdomain]["AAAA"]]
        if "CNAME" in buf[subdomain].keys():
            domain.CNAME = [r.rstrip(".") for r in buf[subdomain]["CNAME"]]
        if "NS" in buf[subdomain].keys():
            domain.NS = [r.rstrip(".") for r in buf[subdomain]["NS"]]
        yield domain


def get_zones(client):
    zones = []
    try:
        zones = client.list_zones()
        zones = list(zones)
    except Exception as e:
        logging.critical(
            f"""Failed to fetch zones from Google Cloud. Could not discover credentials.
Ensure that the environment variable `GOOGLE_APPLICATION_CREDENTIALS` is set to the JSON credential file's location, 
or that the JSON file is in the default location. Also, ensure that the correct project id has been passed.
{e}"""
        )
        exit(-1)

    logging.debug(f"Got {len(zones)} zones from Google Cloud")
    if len(zones) == 0:
        return []

    return zones


def fetch_domains(project_id, **args):
    domains = []

    logger = logging.getLogger("google")
    logger.setLevel(logging.CRITICAL)

    client = dns.Client(project_id)

    zones = get_zones(client)

    for zone in zones:
        try:
            records = get_records(zone)
        except:
            logging.warning(
                f"Could not retrieve records for Google Cloud zone '{zone.dns_name}'"
            )
            records = []
        logging.debug(
            f"Got {len(records)} records for Google Cloud zone '{zone.dns_name}'"
        )

        for domain in convert_records_to_domains(records):
            domains.append(domain)
    logging.warning(f"Got {len(domains)} records from Google Cloud")
    return domains

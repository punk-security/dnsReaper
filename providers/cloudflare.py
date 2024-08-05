import CloudFlare, logging

from domain import Domain

description = "Scan multiple domains by fetching them from Cloudflare"


def get_records(client, zone_id):
    records = []

    page_number = 0
    while True:
        page_number += 1

        # request the DNS records from that zone
        try:
            raw_results = client.zones.dns_records.get(
                zone_id, params={"page": page_number}
            )
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit(f"/zones/dns_records.get api call failed {e}")

        records.extend(raw_results["result"])

        total_pages = raw_results["result_info"]["total_pages"]
        if page_number == total_pages:
            break

    return records


def convert_records_to_domains(records):
    buf = {}

    for record in records:
        if record["name"] not in buf.keys():
            buf[record["name"]] = {}
        if record["type"] not in buf[record["name"]].keys():
            buf[record["name"]][record["type"]] = []
        buf[record["name"]][record["type"]].append(record["content"])

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

    page_number = 0
    while True:
        page_number += 1
        try:
            raw_results = client.zones.get(params={"page": page_number})
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            exit(f"/zones.get api call failed {e}")
        except Exception as e:
            exit(f"/zones.get api call failed {e}")

        zones.extend(raw_results["result"])

        total_pages = raw_results["result_info"]["total_pages"]
        if page_number == total_pages:
            break

    logging.info(f"Got {len(zones)} zones ({total_pages} pages) from cloudflare")

    if len(zones) == 0:
        return []

    return zones


def fetch_domains(cloudflare_token, **args):
    domains = []

    client = CloudFlare.CloudFlare(token=cloudflare_token, raw=True)
    zones = get_zones(client)
    for zone in zones:
        records = get_records(client, zone["id"])
        logging.debug(
            f"Got {len(records)} records for cloudflare zone '{zone['name']}'"
        )
        for record in convert_records_to_domains(records):
            domains.append(record)
    logging.warning(f"Got {len(domains)} records from cloudflare")
    return domains

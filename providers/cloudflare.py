import CloudFlare, logging

from domain import Domain

description = "Scan multiple domains by fetching them from Cloudflare"


def get_records(client, zone_id):
    records = []

    # request the DNS records from that zone
    try:
        records = client.zones.dns_records.get(zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit(f'/zones/dns_records.get api call failed {e}')
    
    return records


def convert_records_to_domains(records):
    buf = {}

    for record in records:
        if record["name"] not in buf.keys():
            buf[record["name"]] = {}
        buf[record["name"]][record["type"]] = [
            record["type"]
        ]
    
    for subdomain in buf.keys():
        domain = Domain(subdomain.rstrip("."), fetch_standard_records=False)
        if "A" in buf[subdomain].keys():
            domain.A = [subdomain.rstrip(".")]
        if "AAAA" in buf[subdomain].keys():
            domain.A = [subdomain.rstrip(".")]
        if "CNAME" in buf[subdomain].keys():
            domain.CNAME = [subdomain.rstrip(".")]
        if "NS" in buf[subdomain].keys():
            domain.NS = [subdomain.rstrip(".")]
        yield domain


def get_zones(client):

    try:
        zones = client.zones.get()
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        exit(f'/zones.get api call failed {e}')
    except Exception as e:
        exit(f'/zones.get api call failed {e}')   
    
    logging.debug(f"Got {len(zones)} zones from cloudflare")

    if len(zones) == 0:
        return []
    
    return zones


def fetch_domains(cloudflare_token, **args):
    domains = []

    client = CloudFlare.CloudFlare(
        token=cloudflare_token
    )
    zones = get_zones(client)
    for zone in zones:
        records = get_records(client, zone["id"])
        logging.debug(f"Got {len(records)} records for cloudflare zone '{zone['name']}'")
        for record in convert_records_to_domains(records):
            domains.append(record)
    return domains

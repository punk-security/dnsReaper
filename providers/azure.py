from azure.mgmt.dns import DnsManagementClient
from azure.identity import ClientSecretCredential

import logging

from domain import Domain

description = "Scan multiple domains by fetching them from Azure DNS services"


def get_records(client, zone):
    records = []
    zone_name = zone[0]
    rg = zone[1].split("/")[4]
    # request the DNS records from that zone
    try:
        records = [
            [
                x.name,
                x.fqdn,
                x.type.split("/")[2],
                x.a_records,
                x.aaaa_records,
                x.caa_records,
                x.cname_record,
                x.mx_records,
                x.ns_records,
                x.ptr_records,
                x.soa_record,
                x.srv_records,
                x.txt_records,
            ]
            for x in client.record_sets.list_by_dns_zone(rg, zone_name)
        ]
    except Exception as e:
        exit(f"/zones/dns_records.get api call failed {e}")

    return records


def convert_records_to_domains(records):
    buf = {}

    for record in records:
        if record[1] not in buf.keys():
            buf[record[1]] = {}
        if record[2] not in buf[record[1]].keys():
            buf[record[1]][record[2]] = []
        if record[2] == "A":
            buf[record[1]][record[2]].append([x.ipv4_address for x in record[3]])
        if record[2] == "AAAA":
            buf[record[1]][record[2]].append([x.ipv6_address for x in record[4]])
        if record[2] == "CNAME":
            buf[record[1]][record[2]].append(record[6])
        if record[2] == "NS":
            buf[record[1]][record[2]].append([x.nsdname for x in record[8]])

    for subdomain in buf.keys():
        domain = Domain(subdomain.rstrip("."), fetch_standard_records=False)
        if "A" in buf[subdomain].keys():
            domain.A = [r.rstrip(".") for r in buf[subdomain]["A"][0]]
        if "AAAA" in buf[subdomain].keys():
            domain.A = [r.rstrip(".") for r in buf[subdomain]["AAAA"][0]]
        if "CNAME" in buf[subdomain].keys():
            domain.CNAME = [r.cname.rstrip(".") for r in buf[subdomain]["CNAME"]]
        if "NS" in buf[subdomain].keys():
            domain.NS = [r.rstrip(".") for r in buf[subdomain]["NS"][0]]
        yield domain


def get_zones(client):
    try:
        zones = [[x.name, x.id] for x in client.zones.list()]
    except Exception as e:
        exit(f"/zones.get api call failed {e}")

    logging.debug(f"Got {len(zones)} zones from Azure")

    if len(zones) == 0:
        return []

    return zones


def fetch_domains(
    az_subscription_id, az_tenant_id, az_client_id, az_client_secret, **args
):
    domains = []
    credentials = ClientSecretCredential(
        az_tenant_id, az_client_id, az_client_secret, **args
    )
    client = DnsManagementClient(
        credentials, az_subscription_id, api_version="2018-05-01"
    )
    zones = get_zones(client)
    for zone in zones:
        records = get_records(client, zone)
        logging.debug(f"Got {len(records)} records for Azure zone '{zone[0]}'")
        for record in convert_records_to_domains(records):
            domains.append(record)
    return domains

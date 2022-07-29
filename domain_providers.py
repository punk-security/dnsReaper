import logging
from domain import Domain

import boto3


def from_file(filename):
    with open(filename) as file:
        try:
            lines = file.readlines()
            logging.info(f"Ingested {len(lines)} domains")
        except Exception as e:
            logging.error(f"Could not read any domains from file {filename} -- {e}")
    return [Domain(line.rstrip()) for line in lines]


def aws_get_records(client, zone_id):
    records = []
    paginator = client.get_paginator("list_resource_record_sets")
    source_zone_records = paginator.paginate(HostedZoneId=zone_id)
    for record_set in source_zone_records:
        records = [*records, *record_set["ResourceRecordSets"]]
    return records


def aws_convert_records_to_domains(records):
    buf = {}
    for record in records:
        if record["Name"] not in buf.keys():
            buf[record["Name"]] = {}
        buf[record["Name"]][record["Type"]] = [
            r["Value"] for r in record["ResourceRecords"]
        ]
    for subdomain in buf.keys():
        domain = Domain(subdomain.rstrip("."), fetch_standard_records=False)
        if "A" in buf[subdomain].keys():
            domain.A = [r.rstrip(".") for r in buf[subdomain]["A"]]
        if "AAAA" in buf[subdomain].keys():
            domain.A = [r.rstrip(".") for r in buf[subdomain]["AAAA"]]
        if "CNAME" in buf[subdomain].keys():
            domain.CNAME = [r.rstrip(".") for r in buf[subdomain]["CNAME"]]
        if "NS" in buf[subdomain].keys():
            domain.NS = [r.rstrip(".") for r in buf[subdomain]["NS"]]
        yield domain


def aws_get_zones(client):
    hosted_zones = client.list_hosted_zones()["HostedZones"]
    logging.debug(f"Got {len(hosted_zones)} zones from aws")
    if len(hosted_zones) == 0:
        return []
    public_zones = [zone for zone in hosted_zones if not zone["Config"]["PrivateZone"]]
    logging.info(f"Got {len(hosted_zones)} public zones from aws")
    if len(public_zones) == 0:
        return []
    return public_zones


def from_aws(access_key_id, access_key_secret):
    domains = []
    client = boto3.client(
        "route53",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=access_key_secret,
    )
    zones = aws_get_zones(client)
    for zone in zones:
        records = aws_get_records(client, zone["Id"].replace("/hostedzone/", ""))
        logging.debug(f"Got {len(records)} records for aws zone '{zone['Name']}'")
        for domain in aws_convert_records_to_domains(records):
            domains.append(domain)
    return domains

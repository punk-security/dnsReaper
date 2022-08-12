import boto3
import logging

from domain import Domain

description = "Scan multiple domains by fetching them from AWS Route53"


def get_records(client, zone_id):
    records = []
    paginator = client.get_paginator("list_resource_record_sets")
    source_zone_records = paginator.paginate(HostedZoneId=zone_id)
    for record_set in source_zone_records:
        records = [*records, *record_set["ResourceRecordSets"]]
    return records


def convert_records_to_domains(records):
    buf = {}
    for record in records:
        if record["Name"] not in buf.keys():
            buf[record["Name"]] = {}
        if "ResourceRecords" in record:
            buf[record["Name"]][record["Type"]] = [
                r["Value"] for r in record["ResourceRecords"]
            ]
        elif "AliasTarget" in record:
            buf[record["Name"]][record["Type"]] = [
                record["AliasTarget"]["DNSName"]
            ]
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
    hosted_zones = client.list_hosted_zones()["HostedZones"]
    logging.debug(f"Got {len(hosted_zones)} zones from aws")
    if len(hosted_zones) == 0:
        return []
    public_zones = [zone for zone in hosted_zones if not zone["Config"]["PrivateZone"]]
    logging.info(f"Got {len(hosted_zones)} public zones from aws")
    if len(public_zones) == 0:
        return []
    return public_zones


def validate_args(aws_access_key_id, aws_access_key_secret):
    if aws_access_key_id is not None and aws_access_key_secret is None:
        raise ValueError("--aws-access-key-secret must be specified if --aws-access-key-id is specified")
    if aws_access_key_secret is not None and aws_access_key_id is None:
        raise ValueError("--aws-access-key-id must be specified if --aws-access-key-secret is specified")


def fetch_domains(aws_access_key_id=None, aws_access_key_secret=None, **args):  # NOSONAR
    validate_args(aws_access_key_id, aws_access_key_secret)
    domains = []
    client = boto3.client(
        "route53",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_access_key_secret,
    )
    zones = get_zones(client)
    for zone in zones:
        records = get_records(client, zone["Id"].replace("/hostedzone/", ""))
        logging.debug(f"Got {len(records)} records for aws zone '{zone['Name']}'")
        for domain in convert_records_to_domains(records):
            domains.append(domain)
    logging.warn(f"Got {len(domains)} records from aws")
    return domains

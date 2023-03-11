import logging

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from domain import Domain

description = "Scan multiple domains by fetching them from AWS Route53"


def get_records(client, zone_id):
    records = []

    try:
        paginator = client.get_paginator("list_resource_record_sets")
        source_zone_records = paginator.paginate(HostedZoneId=zone_id)
    except ClientError as e:
        logging.critical(
            f"Failed to fetch zone records. Ensure you have the 'ListResourceRecordSets' permission on '{zone_id}'. {e}"
        )

        return []

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
            buf[record["Name"]][record["Type"]] = [record["AliasTarget"]["DNSName"]]
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
    hosted_zones = []
    try:
        hosted_zones = client.list_hosted_zones()["HostedZones"]
    except ClientError as e:
        logging.critical(
            f"Failed to fetch zones from AWS. Ensure you have the 'ListHostedZones' permission. {e}"
        )
        exit(-1)

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
        raise ValueError(
            "--aws-access-key-secret must be specified if --aws-access-key-id is specified"
        )
    if aws_access_key_secret is not None and aws_access_key_id is None:
        raise ValueError(
            "--aws-access-key-id must be specified if --aws-access-key-secret is specified"
        )


def fetch_domains(
    aws_access_key_id=None, aws_access_key_secret=None, aws_session_token=None, **args
):
    validate_args(aws_access_key_id, aws_access_key_secret)
    domains = []

    sts_client = boto3.client(
        "sts",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_access_key_secret,
        aws_session_token=aws_session_token,
    )

    try:
        caller_id = sts_client.get_caller_identity()
        logging.warning(f"Using IAM identity: {caller_id['Arn']}")
    except NoCredentialsError:
        logging.critical(
            """
ERROR - Could not locate valid AWS provider credentials. Please provide IAM access keys via the '--aws-access-key-id'
and '--aws-access-key-secret' command-line options or consult the AWS provider documentation for alternative 
authentication methods
"""
        )
        exit(-1)

    client = boto3.client(
        "route53",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_access_key_secret,
        aws_session_token=aws_session_token,
    )
    zones = get_zones(client)
    for zone in zones:
        try:
            records = get_records(client, zone["Id"].replace("/hostedzone/", ""))
        except:
            logging.warning(f"Could not retrieve records for aws zone '{zone['Name']}'")
            records = []
        logging.debug(f"Got {len(records)} records for aws zone '{zone['Name']}'")
        for domain in convert_records_to_domains(records):
            domains.append(domain)
    logging.warning(f"Got {len(domains)} records from aws")
    return domains

import asyncio
import datetime
import logging
import os
import random
import re
import sys
import time
import urllib.parse
import uuid
from functools import partial
from sys import stdout

import boto3

import detection_enums
import output
import signatures
from domain import Domain
from providers import projectdiscovery
from resolver import Resolver
from scan import scan_domain

sys.path.append(os.getcwd())

logger = logging.getLogger()
logger.setLevel("INFO")

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

###### signatures

signatures = [getattr(signatures, signature) for signature in signatures.__all__]

# replace name for each signature
for signature in signatures:
    signature.__name__ = signature.__name__.replace("signatures.", "")

signatures = [
    s for s in signatures if s.test.CONFIDENCE != detection_enums.CONFIDENCE.UNLIKELY
]


@app.get("/")
async def root():
    return {"message": "Hello Punk!"}


@app.get("/check")
async def check(domain: str):
    try:
        logging.warning(f"Received: {domain}")
        domain = domain.replace(" ", "")
        domains = domain.split(",")
        return (await process_domains(domains))["findings"]
    except Exception as e:
        logging.error(f"Caught exception when checking: {e}")

        return {"error": True}


@app.get("/scan")
async def scan(domain: str):
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(DYNAMO_TABLE)
        logging.warning(f"Received: {domain}")
        domain = domain.replace(" ", "")
        domains = domain.split(",")
        results = await process_domains(domains)
        guid = str(uuid.uuid4())
        table.put_item(Item={"guid": guid, "results": results})
        return {"results": guid}
    except Exception as e:
        logging.error(e)
        return {"error": True}


@app.get("/result")
async def result(id: str):
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(DYNAMO_TABLE)
        logging.warning(f"Received id: {id}")
        return table.get_item(Key={"guid": id})["Item"]["results"]
    except Exception as e:
        logging.error(e)
        return {"error": True}


###### scanning

PD_API_KEY = os.environ.get("PD_API_KEY", None)
DYNAMO_TABLE = os.environ.get("DYNAMO_TABLE", None)
SCAN_DOMAIN_LIMIT = os.environ.get("SCAN_DOMAIN_LIMIT", 2000)


async def process_domains(domains: list[str]):
    Domain.resolver = Resolver(
        nameservers=[
            "8.8.8.8",
            "8.8.4.4",
            "1.1.1.1",
            "1.0.0.1",
            "208.67.222.2",
            "208.67.220.2",
        ],
        parallelism=4000,
    )
    findings = []
    domain_objs = [Domain(domain) for domain in domains]
    if len(domains) == 1:
        # Project Discovery!

        primary_domain = domains[0].strip()

        if "://" not in primary_domain:
            # If no scheme is present, add a prefix so urlsplit treats it as absolute
            primary_domain = f"//{primary_domain}"

        # Use urlsplit to remove any URL gubbins
        primary_domain = urllib.parse.urlsplit(primary_domain).hostname

        # urlsplit doesn't do validation. Double check that the hostname doesn't have any undesired chars
        invalid_char_match = re.search("[^a-zA-Z0-9.-]", primary_domain)

        if invalid_char_match is not None:
            return {"error": True, "message": "Invalid domain"}

        # Remove any remaining nonsense characters
        pd_domains = projectdiscovery.fetch_domains(PD_API_KEY, primary_domain)

        logging.warning(f"Got {len(pd_domains)} domains from PD")
        domain_objs += pd_domains

    random.shuffle(domain_objs)
    domain_objs = domain_objs[:SCAN_DOMAIN_LIMIT]
    logging.warning(domain_objs)
    start_time = time.time()
    with output.Output("json", stdout) as o:
        scan = partial(
            scan_domain,
            signatures=signatures,
            output_handler=o,
            findings=findings,
        )
        await asyncio.wait(
            [asyncio.create_task(scan(domain)) for domain in domain_objs],
            timeout=20,
            return_when=asyncio.ALL_COMPLETED,
        )
    return {
        "domains": domains,
        "findings": [f.__dict__ for f in findings],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count_scanned_domains": len(domain_objs),
        "count_signatures": len(signatures),
        "execution_time": str(round(time.time() - start_time, 2)),
    }


def handler(event, context):
    asgi_handler = Mangum(app)
    response = asgi_handler(
        event, context
    )  # Call the instance with the event arguments

    return response

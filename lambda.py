from scan import scan_domain
import signatures
import output
import detection_enums
from providers import projectdiscovery
from domain import Domain
from os import linesep

from multiprocessing.pool import ThreadPool
import threading
from functools import partial

import logging
from sys import stderr, exit, argv, stdout

import time

import sys, os

import asyncio

import random

import uuid
import boto3
import datetime

from resolver2 import Resolver

sys.path.append(os.getcwd())

logger = logging.getLogger()
logger.setLevel("INFO")

from fastapi import FastAPI, Request
from fastapi.responses import Response
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
        return {"error": True}  # f" {e}"}


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
        return {"error": True}  # f" {e}"}


@app.get("/result")
async def result(id: str):
    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(DYNAMO_TABLE)
        logging.warning(f"Received id: {id}")
        return table.get_item(Key={"guid": id})["Item"]["results"]
    except Exception as e:
        logging.error(e)
        return {"error": True}  # f" {e}"}


###### scanning

PD_API_KEY = os.environ.get("PD_API_KEY", None)
DYNAMO_TABLE = os.environ.get("DYNAMO_TABLE", None)


async def process_domains(domains):
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
    Domains = [Domain(domain) for domain in domains]
    if len(domains) == 1:
        # Project Discovery!
        pd_domains = projectdiscovery.fetch_domains(PD_API_KEY, domains[0])
        logging.warning(f"Got {len(pd_domains)} domains from PD")
        Domains = Domains + pd_domains
    # lock = threading.Lock()
    random.shuffle(Domains)
    Domains = Domains[:2000]  # upto 200 domains to test
    logging.warning(Domains)
    start_time = time.time()
    with output.Output("json", stdout) as o:
        scan = partial(
            scan_domain,
            signatures=signatures,
            output_handler=o,
            findings=findings,
        )
        await asyncio.wait(
            [asyncio.create_task(scan(domain)) for domain in Domains],
            timeout=20,
            return_when=asyncio.ALL_COMPLETED,
        )
    return {
        "domains": domains,
        "findings": [f.__dict__ for f in findings],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count_scanned_domains": len(Domains),
        "count_signatures": len(signatures),
        "execution_time": str(round(time.time() - start_time, 2)),
    }


def handler(event, context):
    # if event.get("some-key"):
    # Do something or return, etc.

    asgi_handler = Mangum(app)
    response = asgi_handler(
        event, context
    )  # Call the instance with the event arguments

    return response

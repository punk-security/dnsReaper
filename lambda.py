from scan import scan_domain
import signatures
import output
import detection_enums
import providers
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


sys.path.append(os.getcwd())


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
    s
    for s in signatures
    if s.test.CONFIDENCE != detection_enums.CONFIDENCE.UNLIKELY
]


@app.get("/")
async def root():
    return {"message": "Hello Punk!"}


@app.get("/check")
async def check(domain: str):
    try:
        domain = domain.replace(" ","")
        domains = domain.split(",")
        return await process_domains(domains)
    except Exception as e:
        return {"error": f" {e}"}


###### scanning


async def process_domains(domains):
    findings = []
    Domains = [Domain(domain) for domain in domains]
    # lock = threading.Lock()
    with output.Output("json", stdout) as o:
        scan = partial(
            scan_domain,
            signatures=signatures,
            output_handler=o,
            findings=findings,
            name_servers=[],
        )

        await asyncio.gather(*[asyncio.create_task(scan(domain)) for domain in Domains])
    return findings


def handler(event, context):
    # if event.get("some-key"):
    # Do something or return, etc.

    asgi_handler = Mangum(app)
    response = asgi_handler(
        event, context
    )  # Call the instance with the event arguments

    return response

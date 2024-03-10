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


@app.get("/")
async def root():
    return {"message": "Hello Punk!"}


@app.get("/check")
async def check(domain: str):
    try:
        findings = process_domain(Domain(domain))
        return build_response(findings)
    except Exception as e:
        return {"error": f" {e}"}


###### scanning


def process_domain(domain):
    findings = []
    lock = threading.Lock()
    with output.Output("json", stdout) as o:
        scan_domain(domain, signatures, lock, findings, o, name_servers=[])
        return findings


def build_response(findings):
    msg = f"We found {len(findings)} takeovers ☠️"
    for finding in findings:
        msg += f"-- DOMAIN '{finding.domain}' :: SIGNATURE '{finding.signature}' :: CONFIDENCE '{finding.confidence}'"
        msg += f"{linesep}{finding.populated_records()}"
    return msg


def handler(event, context):
    # if event.get("some-key"):
    # Do something or return, etc.

    asgi_handler = Mangum(app)
    response = asgi_handler(
        event, context
    )  # Call the instance with the event arguments

    return response

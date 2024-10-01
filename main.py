#!/usr/bin/env python3
from scan import scan_domain
import signatures
import output
import detection_enums
import providers
from os import linesep
from domain import Domain
from resolver import Resolver

from functools import partial

import logging
from sys import stderr, exit, argv

import argparsing

import colorama

import time

import asyncio

import dns.resolver

start_time = time.time()

if "--nocolour" in argv:
    print(argparsing.banner, file=stderr)
else:
    colorama.init()
    print(argparsing.banner_with_colour, file=stderr)

args = argparsing.parse_args()

###### verbosity

if args.verbose == 0:
    verbosity_level = logging.WARN
if args.verbose == 1:
    verbosity_level = logging.INFO
if args.verbose > 1:
    verbosity_level = logging.DEBUG

logging.basicConfig(format="%(message)s", level=verbosity_level)
logging.StreamHandler(stderr)

if not args.verbose > 2:
    for module in ["boto", "requests"]:
        logger = logging.getLogger(module)
        logger.setLevel(logging.CRITICAL)

###### signatures

signatures = [getattr(signatures, signature) for signature in signatures.__all__]

# replace name for each signature
for signature in signatures:
    signature.__name__ = signature.__name__.replace("signatures.", "")

if args.signature:
    signatures = [s for s in signatures if s.__name__ in args.signature]

if args.exclude_signature:
    signatures = [s for s in signatures if s.__name__ not in args.exclude_signature]

if not args.enable_unlikely:
    signatures = [
        s
        for s in signatures
        if s.test.CONFIDENCE != detection_enums.CONFIDENCE.UNLIKELY
    ]

if args.disable_probable:
    signatures = [
        s
        for s in signatures
        if s.test.CONFIDENCE != detection_enums.CONFIDENCE.POTENTIAL
    ]

logging.warning(f"Testing with {len(signatures)} signatures")


###### scanning

findings = []

if "--out" not in argv:
    # using default out location, need to append our format
    args.out = f"{args.out}.{args.out_format}"


async def main():
    ###### domain ingestion
    nameservers = (
        dns.resolver.Resolver().nameservers
        if args.resolver == ""
        else args.resolver.replace(" ", "").split(",")
    )
    Domain.resolver = Resolver(nameservers=nameservers, parallelism=args.parallelism)
    provider = getattr(providers, args.provider)
    domains = list(provider.fetch_domains(**args.__dict__))

    if len(domains) == 0:
        logging.error("ERROR: No domains to scan")
        exit(-1)

    with output.Output(args.out_format, args.out) as o:
        scan = partial(
            scan_domain,
            signatures=signatures,
            output_handler=o,
            findings=findings,
        )

        await asyncio.gather(*[asyncio.create_task(scan(domain)) for domain in domains])

    ###### exit
    logging.warning(f"\n\nWe found {len(findings)} takeovers ☠️")
    for finding in findings:
        msg = f"-- DOMAIN '{finding.domain}' :: SIGNATURE '{finding.signature}' :: CONFIDENCE '{finding.confidence}'"
        msg += f"{linesep}{finding.populated_records()}"
        if args.nocolour == False:
            msg = colorama.Fore.RED + msg + colorama.Fore.RESET
            logging.warning(msg)
    logging.warning(
        f"\n⏱️  We completed in {round(time.time() - start_time, 2)} seconds"
    )
    logging.warning(f"...Thats all folks!")
    if args.pipeline:
        logging.debug(f"Pipeline flag set - Exit code: {len(findings)}")
        exit(len(findings))


asyncio.run(main())

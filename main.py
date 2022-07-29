from finding import Finding
import signatures
from domain import Domain
import output
import detection_enums

from multiprocessing.pool import ThreadPool
import threading
from functools import partial

import logging
from sys import stderr, exit

import argparsing

print(argparsing.banner, file=stderr)
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
###### domain ingestion

## file

if args.provider == "file":

    def read_domains(filename):
        with open(filename) as file:
            try:
                lines = file.readlines()
                logging.info(f"Ingested {len(lines)} domains")
            except Exception as e:
                logging.error(f"Could not read any domains from file {filename} -- {e}")
        return [Domain(line.rstrip()) for line in lines]

    domains = read_domains(args.filename)


###### signatures

signatures = [getattr(signatures, signature) for signature in signatures.__all__]

# replace name for each signature
for signature in signatures:
    signature.__name__ = signature.__name__.replace("signatures.", "")

if args.signature:
    signatures = [s for s in signatures if s.__name__ in args.signature]

if args.exclude_signature:
    signatures = [s for s in signatures if s.__name__ not in args.exclude_signature]

if args.disable_unlikely:
    signatures = [
        s for s in signatures if s.CONFIDENCE != detection_enums.CONFIDENCE.UNLIKELY
    ]

if args.disable_probable:
    signatures = [
        s for s in signatures if s.CONFIDENCE != detection_enums.CONFIDENCE.POTENTIAL
    ]

logging.info(f"Testing with {len(signatures)} signatures")


def scan_domain(d, output_handler: output.Output):
    global lock
    global findings
    for signature in signatures:
        logging.debug(
            f"Testing domain '{d.domain}' with signature '{signature.__name__}'"
        )
        if signature.test.potential(domain=d):
            logging.debug(
                f"Potential takeover found on DOMAIN '{d}' using signature '{signature.__name__}'"
            )
            if signature.test.check(domain=d):
                status = signature.test.CONFIDENCE.value
                logging.info(
                    f"Takeover {status} on {d} using signature '{signature.__name__}'"
                )
                finding = Finding(
                    domain=d.domain,
                    signature=signature.__name__,
                    info=signature.test.INFO,
                    confidence=signature.test.CONFIDENCE,
                )
                with lock:
                    findings.append(finding)
                    output_handler.write(finding)
            else:
                logging.debug(
                    f"Takeover not possible on DOMAIN '{d}' using signature '{signature.__name__}'"
                )


global lock
global findings
findings = []
lock = threading.Lock()
with output.Output(args.out_format, args.out) as o:
    scan = partial(scan_domain, output_handler=o)
    pool = ThreadPool(processes=args.parallelism)
    pool.map(scan, domains)

logging.info(f"\n\nWe found {len(findings)} takeovers ☠️")
logging.warning(f"\n...Thats all folks!")

if args.pipeline:
    logging.debug(f"Pipeline flag set - Exit code: {len(findings)}")
    exit(len(findings))

# TOFO: test empire-alpha.integ.amazon.com , dipper-cts-gamma-tcp.aws.amazon.com

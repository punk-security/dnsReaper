import signatures
from domain import Domain

from multiprocessing.pool import ThreadPool

import logging

logging.basicConfig(level=logging.DEBUG)

signatures = [getattr(signatures, signature) for signature in signatures.__all__]


domains = ["punksecurity.io", "punksecurity.co.uk"]


def scan_domain(domain):
    d = Domain(domain)
    for signature in signatures:
        logging.debug(
            f"Testing domain '{domain}' with signature '{signature.__name__}'"
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
                print(domain, signature.test.INFO)


pool = ThreadPool(processes=50)
pool.map(scan_domain, domains)

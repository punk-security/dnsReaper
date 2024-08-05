import logging
from domain import Domain

description = "Scan a single domain by providing a domain on the commandline"


def fetch_domains(domain, **args):
    logging.warning(f"Domain '{domain}' provided on commandline")
    return [Domain(domain)]

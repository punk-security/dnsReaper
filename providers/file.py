import logging
from domain import Domain

description = "Read domains from a file, one per line"


def fetch_domains(filename, **args):
    with open(filename) as file:
        try:
            lines = file.readlines()
            logging.warn(f"Ingested {len(lines)} domains from file '{filename}'")
        except Exception as e:
            logging.error(f"Could not read any domains from file {filename} -- {e}")
    return [Domain(line.rstrip()) for line in lines]

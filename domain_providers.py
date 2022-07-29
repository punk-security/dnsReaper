import logging
from domain import Domain


def from_file(filename):
    with open(filename) as file:
        try:
            lines = file.readlines()
            logging.info(f"Ingested {len(lines)} domains")
        except Exception as e:
            logging.error(f"Could not read any domains from file {filename} -- {e}")
    return [Domain(line.rstrip()) for line in lines]

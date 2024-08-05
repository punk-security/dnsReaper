import logging
from domain import Domain
from os import listdir
from os.path import isfile, join

description = "Read domains from a file (or folder of files), one per line"


def fetch_domains(filename, **args):
    if isfile(filename):
        with open(filename) as file:
            try:
                domains = file.readlines()
                logging.warning(
                    f"Ingested {len(domains)} domains from file '{filename}'"
                )
            except Exception as e:
                logging.error(f"Could not read any domains from file {filename} -- {e}")
                exit(-1)
    else:
        domains = []
        files = fetch_nested_files(filename)
        for f in files:
            try:
                with open(f) as file:
                    domains += file.readlines()
                logging.debug(f"Ingested domains from file '{file}'")
            except:
                logging.debug(f"Could not read file '{file}'")
        logging.warning(f"Ingested {len(domains)} domains from folder '{filename}'")
    return [Domain(domain.rstrip()) for domain in domains]


def fetch_nested_files(dir):
    files = []
    for item in listdir(dir):
        path = join(dir, item)
        if isfile(path):
            files.append(path)
        else:
            files = [*files, *fetch_nested_files(path)]
    return files

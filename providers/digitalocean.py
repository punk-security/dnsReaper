import boto3
import logging

import requests

from domain import Domain

description = "Scan multiple domains by fetching them from Digital Ocean"


class DomainNotFoundError(BaseException):
    def __init__(self, domain):
        self.message = "Domain not found: " + domain
        super().__init__(self.message)


class DoApi:
    def __init__(self, api_key):
        self.session = requests.session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
        )

    @staticmethod
    def check_response(response: requests.Response):
        if response.status_code == 401:
            raise ValueError("Invalid API key specified.")

        if response.status_code < 200 or response.status_code >= 300:
            raise ValueError("Invalid response received from API: " + response.json())

        return response

    def make_request(self, endpoint):
        return self.session.prepare_request(
            requests.Request("GET", "https://api.digitalocean.com/v2/" + endpoint)
        )

    def list_domains(self):
        req = self.make_request("domains")

        return self.check_response(self.session.send(req))

    def get_records(self, domain):
        req = self.make_request(f"domains/{domain}/records")
        res = self.session.send(req)

        if 404 == res.status_code:
            raise DomainNotFoundError(domain)

        return self.check_response(res)


def convert_records_to_domains(records, root_domain):
    buf = {}
    for record in records:
        if "@" == record["name"]:
            continue

        record_name = f"{record['name']}.{root_domain}"

        if record_name not in buf.keys():
            buf[record_name] = {}

        if record["type"] not in buf[record_name].keys():
            buf[record_name][record["type"]] = []

        if "data" in record.keys():
            buf[record_name][record["type"]].append(record["data"])

    def extract_records(desired_type):
        return [r.rstrip(".") for r in buf[subdomain][desired_type]]

    for subdomain in buf.keys():
        domain = Domain(subdomain.rstrip("."), fetch_standard_records=False)

        if "A" in buf[subdomain].keys():
            domain.A = extract_records("A")
        if "AAAA" in buf[subdomain].keys():
            domain.AAAA = extract_records("AAAA")
        if "CNAME" in buf[subdomain].keys():
            domain.CNAME = extract_records("CNAME")
        if "NS" in buf[subdomain].keys():
            domain.NS = extract_records("NS")

        yield domain


def validate_args(do_api_key: str):
    if not do_api_key.startswith("dop_v1"):
        raise ValueError("DigitalOcean: Invalid API key specified")


def fetch_domains(do_api_key: str, do_domains: str = None, **args):  # NOSONAR
    validate_args(do_api_key)
    root_domains = []
    domains = []
    api = DoApi(do_api_key)

    if do_domains is not None and len(do_domains):
        root_domains = [domain.strip(" ") for domain in do_domains.split(",")]
    else:
        resp_data = api.list_domains().json()
        root_domains = [domain["name"] for domain in resp_data["domains"]]

    for domain in root_domains:
        if "" == domain or domain is None:
            continue

        records = api.get_records(domain).json()
        domains.extend(convert_records_to_domains(records["domain_records"], domain))

    return domains

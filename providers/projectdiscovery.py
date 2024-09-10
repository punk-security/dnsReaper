import requests, logging, json

from domain import Domain

description = "Scan multiple domains by fetching them from ProjectDiscovery"


class DomainNotFoundError(Exception):
    def __init__(self, domain):
        self.message = "Domain not found: " + domain
        super().__init__(self.message)


class PDApi:
    def __init__(self, api_key):
        self.session = requests.session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Authorization": api_key}
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
            requests.Request("GET", "https://dns.projectdiscovery.io/dns/" + endpoint)
        )

    def list_domains(self):
        req = self.make_request("domains")

        return self.check_response(self.session.send(req))

    def get_subdomains(self, domain):
        domain = domain.lower()
        req = self.make_request(f"{domain}/subdomains")
        res = self.session.send(req)

        if 404 == res.status_code:
            raise DomainNotFoundError(domain)

        return self.check_response(res)


def fetch_domains(pd_api_key: str, pd_domains: str, **args):
    root_domains = []
    domains = []
    api = PDApi(pd_api_key)

    root_domains = [domain.strip(" ") for domain in pd_domains.split(",")]

    for domain in root_domains:
        if "" == domain or domain is None:
            continue

        raw_domains = api.get_subdomains(domain).json()
        logging.warning(f"Testing {len(raw_domains['subdomains'])} subdomains")
        domains.extend(
            [
                Domain(f"{sb}.{domain}")
                for sb in raw_domains["subdomains"]
                if "*" not in sb
            ]
        )

    return domains

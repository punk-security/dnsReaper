import requests, logging

from domain import Domain

description = "Scan multiple domains by fetching them from Security Trails"


class DomainNotFoundError(Exception):
    def __init__(self, domain):
        self.message = "Domain not found: " + domain
        super().__init__(self.message)


class STApi:
    def __init__(self, api_key):
        self.session = requests.session()
        self.session.headers.update({"accept": "application/json", "APIKEY": api_key})

    @staticmethod
    def check_response(response: requests.Response):
        if response.status_code == 403 and (
            "Invalid authentication credentials" in (response.content).decode("utf-8")
        ):
            raise ValueError(
                "Invalid authentication credentials. Please ensure the API key entered vis correct."
            )

        if response.status_code == 403:
            raise ValueError(
                "This feature is not available for your subscription package. Consider upgrading your package or contact support@securitytrails.com."
            )

        if response.status_code < 200 or response.status_code >= 300:
            raise ValueError("Invalid response received from API: " + response.json())

        return response

    def make_request(self, endpoint):
        return self.session.prepare_request(
            requests.Request("GET", "https://api.securitytrails.com/v1/" + endpoint)
        )

    def get_subdomains(self, domain):
        req = self.make_request(f"domain/{domain}/subdomains")
        res = self.session.send(req)

        if 404 == res.status_code:
            raise DomainNotFoundError(domain)

        return self.check_response(res)


def fetch_domains(st_api_key: str, st_domains: str, **args):
    root_domains = []
    domains = []
    api = STApi(st_api_key)

    root_domains = [domain.strip(" ") for domain in st_domains.split(",")]

    for domain in root_domains:
        if "" == domain or domain is None:
            continue

        raw_domains = api.get_subdomains(domain).json()

        logging.warning(f"Testing {raw_domains['subdomain_count']} subdomains")
        domains.extend([Domain(f"{sb}.{domain}") for sb in raw_domains["subdomains"]])

    return domains

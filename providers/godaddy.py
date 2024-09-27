import requests

from domain import Domain

description = "Scan multiple domains by fetching them from GoDaddy"


class DomainNotFoundError(Exception):
    def __init__(self, domain):
        self.message = "Domain not found: " + domain
        super().__init__(self.message)


class GDApi:
    def __init__(self, api_key, api_secret):
        self.session = requests.session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Authorization": "sso-key " + api_key + ":" + api_secret,
            }
        )

    @staticmethod
    def check_response(response: requests.Response):
        if response.status_code == 401:
            raise ValueError("Invalid API key specified.")
        if response.status_code == 403:
            raise ValueError(
                "API key valid but access denied. GoDaddy now block API access unless you have at least 10 domains"
            )
        if response.status_code < 200 or response.status_code >= 300:
            raise ValueError(
                "Invalid response received from API: " + str(response.json())
            )

        return response

    def make_request(self, endpoint):
        return self.session.prepare_request(
            requests.Request("GET", "https://api.godaddy.com/v1/" + endpoint)
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
            domain.CNAME = [
                x.replace("@", root_domain) for x in extract_records("CNAME")
            ]
        if "NS" in buf[subdomain].keys():
            domain.NS = extract_records("NS")
        yield domain


def fetch_domains(gd_api_key: str, gd_api_secret: str, gd_domains: str = None, **args):
    root_domains = []
    domains = []
    api = GDApi(gd_api_key, gd_api_secret)

    if gd_domains is not None and len(gd_domains):
        root_domains = [domain.strip(" ") for domain in gd_domains.split(",")]
    else:
        resp_data = api.list_domains().json()
        root_domains = [domain["domain"] for domain in resp_data]

    for domain in root_domains:
        if "" == domain or domain is None:
            continue

        records = api.get_records(domain).json()
        domains.extend(convert_records_to_domains(records, domain))

    return domains

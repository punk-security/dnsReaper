import requests

from domain import Domain
from google.cloud import dns
from google.cloud.client import ClientWithProject
from google.cloud.exceptions import NotFound


#TODO: auth

description = "Scan multiple domains by fetching them from Google Cloud"


class DomainNotFoundError(Exception):
    def __init__(self, domain):
        self.message = "Domain not found: " + domain
        super().__init__(self.message)


class DoApi:
    def __init__(self, api_key):
        self.session = requests.session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
        )

    def auth_client(
        project=None, # Opt
        credentials=None, # Opt, Creditals class
        _http=None, 
        client_options=None
    ):
        client = dns.Client()


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
    
    ###
    def get_zone(project_id, name):
        client = dns.Client(project=project_id)
        zone = client.zone(name=name)

        try:
            zone.reload()
            return zone
        except NotFound:
            return None
        
    def list_zones(project_id):
        client = dns.Client(project=project_id)
        zones = client.list_zones()
        return [zone.name for zone in zones]
    
    def list_resource_records(project_id, zone_name):
        client = dns.Client(project=project_id)
        zone = client.zone(zone_name)

        records = zone.list_resource_record_sets()

        return [
            (record.name, record.record_type, record.ttl, record.rrdatas)
            for record in records
        ]
    
    def get_command(args):
        """Gets a zone by name."""
        zone = get_zone(args.project_id, args.name)
        if not zone:
            print("Zone not found.")
        else:
            print("Zone: {}, {}, {}".format(zone.name, zone.dns_name, zone.description))


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


def validate_args(gc_api_key: str):
    if not gc_api_key.startswith("dop_v1"):
        raise ValueError("Google Cloud: Invalid API key specified")
    
def grant_auth(gc_client_id: str):
    authParams = {
        'response_type' : 'token', 
        'client_id' : gc_client_id+'.apps.googleusercontent.com',
        'immediate' : True,
        'scope' : ['https://www.googleapis.com/auth/ndev.clouddns.readonly']
    }

dns.


def fetch_domains(project: str, gc_client_id: str, gc_secret: str, gc_domains: str = None, **args):  # NOSONAR
    grant_auth(gc_client_id)
    validate_args(gc_secret)
    root_domains = []
    domains = []
    api = DoApi(gc_secret)

    if gc_domains is not None and len(gc_domains):
        root_domains = [domain.strip(" ") for domain in gc_domains.split(",")]
    else:
        resp_data = api.list_domains().json()
        root_domains = [domain["name"] for domain in resp_data["domains"]]

    for domain in root_domains:
        if "" == domain or domain is None:
            continue

        records = api.get_records(domain).json()
        domains.extend(convert_records_to_domains(records["domain_records"], domain))

    return domains

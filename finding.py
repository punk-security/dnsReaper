class Finding(object):
    def __init__(self, domain, signature, info, confidence, more_info_url):
        self.domain = domain.domain
        self.signature = signature
        self.info = info.replace("\n", " ").replace("\r", "").rstrip()
        self.confidence = confidence.name
        self.a_records = domain.A
        self.aaaa_records = domain.AAAA
        self.cname_records = domain.CNAME
        self.ns_records = domain.NS
        self.more_info_url = more_info_url

    def populated_records(self):
        resp = ""
        if self.a_records:
            resp += f"A: {self.a_records},"
        if self.aaaa_records:
            resp += f"AAAA: {self.aaaa_records},"
        if self.cname_records:
            resp += f"CNAME: {self.cname_records},"
        if self.ns_records:
            resp += f"NS: {self.ns_records},"
        return resp.rstrip(",")

class Finding(object):
    def __init__(self, domain, signature, info, confidence):
        self.domain = domain
        self.signature = signature
        self.info = info.replace("\n", " ").replace("\r", "").rstrip()
        self.confidence = confidence.name

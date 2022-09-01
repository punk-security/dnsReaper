# Zone Transfer

## Description
The ZoneTransfer provider connects to a DNS Servers and attempts to fetch all records for a given domain.

It requires 2 parameters, and both are mandatory.  Zone Transfers must fetch a single DNS zone, there is no mechanism in the spec to enumerate all zones on the DNS server.

The DNS server should permit Zone Transfers to your IP.  There is no auth mechanism in the zone transfer spec so it operates on an ip allowlist.  You also need TCP Port 53 access to the server, not UDP.

# Usage
zonetransfer_nameserver, zonetransfer_domain
The `--zonetransfer-nameserver` option is used to provide your DNS server fqdn (such as ns1.domain.com) or DNS server IP. ).


The `--zonetransfer-domain` option is used to specify the domain to fetch.  This should be the root domain, i.e. a domain of punksecurity.co.uk would be used to fetch all subdomains such as www.punksecurity.co.uk.  


[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/punk-security/secret-magpie-cli/graphs/commit-activity)
[![Maintaner](https://img.shields.io/badge/maintainer-PunkSecurity-blue)](https://www.punksecurity.co.uk)
[![Docker Pulls](https://img.shields.io/docker/pulls/punksecurity/dnsreaper)](https://hub.docker.com/r/punksecurity/dnsreaper)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=punk-security_dnsReaper&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=punk-security_dnsReaper)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=punk-security_dnsReaper&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=punk-security_dnsReaper)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=punk-security_dnsReaper&metric=bugs)](https://sonarcloud.io/summary/new_code?id=punk-security_dnsReaper)

# DNS Reaper

DNS Reaper is yet another sub-domain takeover tool, but with an emphasis on accuracy, speed and the number of signatures in our arsenal!

We can scan around 50 subdomains per second, testing each one with over 50 takeover signatures.
This means most organisations can scan their entire DNS estate in less than 10 seconds.

### You can use DNS Reaper as an attacker or bug hunter!

 You can run it by providing a list of domains in a file, or a single domain on the command line.  DNS Reaper will then scan the domains with all of its signatures, producing a CSV file.

### You can use DNS Reaper as a defender! 

You can run it by letting it fetch your DNS records for you!  Yes that right, you can run it with credentials and test all your domain config quickly and easily.  DNS Reaper will connect to the DNS provider and fetch all your records, and then test them.

Currently we support AWS Route53.

### You can use DNS Reaper as a DevSecOps Pro!
[Punk Security](https://www.punksecurity.co.uk) are a DevSecOps company, and DNS Reaper has its roots in modern security best practice.

You can run DNS Reaper in a pipeline, feeding it a list of domains that you intend to provision and it will exit Non-Zero if it detects a takeover is possible.  You can prevent takeovers before they are even possible!

## Usage 

To run DNS Reaper, you can use the docker image or run it with python 3.10.

### Run it with docker

``` docker run punksecurity/dnsreaper --help  ```

### Run it with python
``` 
pip install -m requirements
python main.py --help
```

### Common commands

* Scan AWS account:

    ``` docker run punksecurity/dnsreaper aws --aws-aws-access-key-id <key> --aws-access-key-secret <secret> ```
* Scan all domains from file:

    ``` docker run punksecurity/dnsreaper file --filename <filename> ```
* Scan single domain

    ``` docker run punksecurity/dnsreaper single --domain <domain> ```
* Scan single domain and output to stdout:

    You should either redirect the stderr output or save stdout output with >

    ``` docker run punksecurity/dnsreaper single --domain <domain> --out stdout --out-format=json > output```
### Full usage

```
          ____              __   _____                      _ __
         / __ \__  ______  / /__/ ___/___  _______  _______(_) /___  __
        / /_/ / / / / __ \/ //_/\__ \/ _ \/ ___/ / / / ___/ / __/ / / /
       / ____/ /_/ / / / / ,<  ___/ /  __/ /__/ /_/ / /  / / /_/ /_/ /
      /_/    \__,_/_/ /_/_/|_|/____/\___/\___/\__,_/_/  /_/\__/\__, /
                                             PRESENTS         /____/
                              DNS Reaper ☠️

             Scan all your DNS records for subdomain takeovers!

usage:
main.py provider [options]

help:
main.py --help

providers:
  > aws - Scan multiple domains by fetching them from AWS Route53
  > bind - Read domains from a dns BIND zone file, or path to multiple
  > cloudflare - Scan multiple domains by fetching them from Cloudflare
  > file - Read domains from a file, one per line
  > single - Scan a single domain by providing a domain on the commandline

positional arguments:
  {aws,bind,cloudflare,file,single}

options:
  -h, --help            show this help message and exit
  --out OUT             Output file (default: results) - use 'stdout' to stream out
  --out-format {csv,json}
  --parallelism PARALLELISM
                        Number of domains to test in parallel - too high and you may see odd DNS results (default: 30)
  --disable-probable    Do not check for probable conditions
  --enable-unlikely     Check for more conditions, but with a high false positive rate
  --signature SIGNATURE
                        Only scan with this signature (multiple accepted)
  --exclude-signature EXCLUDE_SIGNATURE
                        Do not scan with this signature (multiple accepted)
  --pipeline            Exit Non-Zero on detection (used to fail a pipeline)
  -v, --verbose         -v for verbose, -vv for extra verbose
  --nocolour            Turns off coloured text

aws:
  Scan multiple domains by fetching them from AWS Route53

  --aws-access-key-id AWS_ACCESS_KEY_ID
  --aws-access-key-secret AWS_ACCESS_KEY_SECRET

bind:
  Read domains from a dns BIND zone file, or path to multiple

  --bind-zone-file BIND_ZONE_FILE

cloudflare:
  Scan multiple domains by fetching them from Cloudflare

  --cloudflare-token CLOUDFLARE_TOKEN

file:
  Read domains from a file, one per line

  --filename FILENAME

single:
  Scan a single domain by providing a domain on the commandline

  --domain DOMAIN
```
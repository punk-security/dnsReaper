# DigitalOcean

## Description
The DigitalOcean provider connects to the DigitalOcean API and retrieves domains and records.
It can enumerate all available domains, or alternatively you can supply a comma-separated list of domains to limit
the scope to.

# Usage
The `--do-api-key` option is used to provide your DigitalOcean API Key. API keys are available from the DigitalOcean
control panel (click API in the sidebar, or [here for a direct link](https://cloud.digitalocean.com/account/api/tokens)).

The API key should be limited to read-only access.

The `--do-domains` option is used to limit the domains that are being scanned. Multiple domains can be provided by separating
each domain with a comma, eg:
`--do-domains first.domain.example,second.domain.example`

# Security Trails

## Description
The SecurityTrails provider connects to the SecurityTrails API and retrieves subdomains associated with a domain.

To enumerate a domain's subdomains, you need to provide a valid API key.

## Usage
The `--st-api-key` option is used to provide you SecurityTrail API Key. API keys are available from the SecurityTrail user account page (click on API in the sidebar, then the API Keys tab, or [click here](https://securitytrails.com/app/account/credentials) for a direct link).

The `--st-domains` option is used to list the domains that are to be scanned. Multiple domains can be provided by separating each domain with a comma, e.g:

`--st-domains first.domain.example,second.domain.example`

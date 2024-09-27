# GoDaddy

## WARNING: GoDaddy now block API access unless you have 10 domains and email their support. Craaaazy!

## Description
The GoDaddy provider connects to the GoDaddy API and retrieves domains and records.

It can enumerate all available domains, or alternatively you can supply a comma-separated list of domains to limit
the scope to.

## Create a GoDaddy API Key and Secret
To get started creating an API Key and Secret,

1. Log in to your GoDaddy account
2. Navigate to `https://developer.godaddy.com/`
3. Select API Keys
4. Click the **Create New API key button**
5. Give the API Key a name (if required) and under `Environment`, select an appropriate option. If you are unsure, select `Production`
6. Make a note of the `API Key` and `API Secret`. **The secret is only viewable once, so make sure the note it down**

## Usage
The `--gd-api-key` option is used to provide your GoDaddy API Key. API keys are available from the GoDaddy
developer console ([click here for a direct link](https://developer.godaddy.com/keys)).

The `--gd-api-secret` option is used to provide your GoDaddy API Secret.

The `--gd-domains` option is used to limit the domains that are being scanned. Multiple domains can be provided by separating
each domain with a comma, eg:
`--gd-domains first.domain.example,second.domain.example`

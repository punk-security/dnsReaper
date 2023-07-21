# Project Discovery

## Description
The Project Discovery provider connects to the Project Discovery API and retrieves subdomains associated with a domain.

To enumerate a domain's subdomains, you need to provide a valid API key.

## Acquire a Project Discovery API Key
To get a Project Discovery API Key,

1. Navigate to the [Project Discovery](https://projectdiscovery.io/) webpage
2. Scrolling down to the `Chaos` section
3. Click the **Request key** button
4. Complete the form
5. If they grant you access, an email containing your API key will be sent to your email.


## Usage
The `--pd-api-key` option is used to provide you Project Discovery API Key. An API keys can be acquired by visiting the Project Discovery webpage and requesting one.

The `--pd-domains` option is used to list the domains that are to be scanned. Multiple domains can be provided by separating each domain with a comma, e.g:

`--pd-domains first.domain.example,second.domain.example`

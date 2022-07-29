# Providers

Providers provide the domains to the scanning engine, wether they are read from the cli, a local file or a service provider.

All providers have two mandatory items, a description and a fetch_domains function.

```
description = "This is a description of the provider"

def fetch_domains(argumentA, argumentB **args):
    #do sometyhing
    return [Domain(domain)]
```

The description and provider file name are used to configure the argument parser and help menu.

The fetch_domains function can take any number of arguments, and these are automatically added to the argument parsers and help menu.

#### IMPORTANT:  All providers must have unique argument names (so considering namespacing them such as ```<provider>_access_key``` rather than ```access_key``` )

## Adding a new provider

1. Create a new .py file in providers
2. Add a description
3. Add a fetch_domains function that returns a list of ```domain.Domain``` objects or an empty list
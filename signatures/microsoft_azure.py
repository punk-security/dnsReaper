from .routine.cname_found_but_NX_DOMAIN import cname_found_but_NX_DOMAIN

cnames = [
    ".cloudapp.net",
    ".cloudapp.azure.com",
    ".azurewebsites.net",
    ".blob.core.windows.net",
    ".cloudapp.azure.com",
    ".azure-api.net",
    ".azurehdinsight.net",
    ".azureedge.net",
    ".azurecontainer.io",
    ".database.windows.net",
    ".azuredatalakestore.net",
    ".search.windows.net",
    ".azurecr.io",
    ".redis.cache.windows.net",
    ".azurehdinsight.net",
    ".servicebus.windows.net",
]

INFO = """
The defined domain has CNAME records configured for Microsoft Azure but they dont exist at Azure. \
An attacker can register this domain on Microsoft Azure.

    """

test = cname_found_but_NX_DOMAIN(
    cname=cnames,
    info=INFO,
)

check = test.check
potential = test.potential
CONFIDENCE = test.CONFIDENCE
INFO = test.INFO

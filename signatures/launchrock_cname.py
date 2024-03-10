from .templates.cname_found_but_status_code import cname_found_but_status_code

test = cname_found_but_status_code(
    cname="host.launchrock.com",
    code=0,
    service="Launchrock",
    https=True,
)

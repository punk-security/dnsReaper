from .templates.cname_found_but_status_code import cname_found_but_status_code

test = cname_found_but_status_code(
    cname="cname.launchrock.com",
    code=500,
    service="Launchrock",
    https=True,
)

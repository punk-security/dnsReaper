from .templates.cname_found_but_status_code import cname_found_but_status_code

test = cname_found_but_status_code(
    cname="domains.bettermode.io",
    code=409,
    service="bettermode.com",
)

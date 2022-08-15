from .templates.cname_found_but_status_code import cname_found_but_status_code

test = cname_found_but_status_code(
    cname="cname.announcekit.app",
    code=0,  # status code 0 on tls falure
    service="announcekit",
)

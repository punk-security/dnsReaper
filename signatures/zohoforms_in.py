from .templates.cname_found_but_status_code import cname_found_but_status_code

test = cname_found_but_status_code(
    cname=[
        "forms.cs.zohohost.in",
    ],
    service="zoho forms india",
    code=403,
)

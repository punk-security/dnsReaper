from .templates.cname_found_but_status_code import cname_found_but_status_code

test = cname_found_but_status_code(
    cname=[
        "forms.cs.zohohost.com",
        "forms.cs.zohohost.eu",
    ],
    service="zoho forms",
    code=400,
)

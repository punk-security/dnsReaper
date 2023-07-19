from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=".cargo.site",
    domain_not_configured_message="""<div class="notfound">\n\t\t\t404 Not Found<br>\n\t\t\t<a class="homepage_link""",
    service="Cargo Collective",
)

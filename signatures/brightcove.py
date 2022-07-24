from .templates.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname=[".bcvp0rtal.com", ".brightcovegallery.com", ".gallery.video"],
    domain_not_configured_message="Page Not Found",
    service="BrightCove",
)

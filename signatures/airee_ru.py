from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

test = cname_found_but_string_in_body(
    cname="cdn.airee.ru",
    domain_not_configured_message="Ошибка 402. Сервис Айри.рф не оплачен",
    service="airee.ru",
)

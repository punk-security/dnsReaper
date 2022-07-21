from .routine.cname_found_but_string_in_body import cname_found_but_string_in_body

INFO = """
The defined domain has CNAME records configured for airee.ru and is not claimed. \
An attacker can register this domain on airee.ru.

    """

test = cname_found_but_string_in_body(
    cname="cdn.airee.ru",
    domain_not_configured_message="Ошибка 402. Сервис Айри.рф не оплачен",
    info=INFO,
)

check = test.check
potential = test.potential
CONFIDENCE = test.CONFIDENCE
INFO = test.INFO

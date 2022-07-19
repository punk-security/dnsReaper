from collections import namedtuple
from domain import Domain


def mock_web_response(body="", status_code=0):
    def mock_fetch_web(**kwargs):
        return namedtuple("web_response", ["body", "status_code"])(body, status_code)

    domain = Domain("mock.local", fetch_standard_records=False)
    domain.fetch_web = mock_fetch_web
    return domain

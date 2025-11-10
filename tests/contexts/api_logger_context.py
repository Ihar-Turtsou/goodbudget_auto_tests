from utils import api_logging
from utils.logger_allure import attach_request, attach_response
from utils.logger_console import log_response


class ApiLogger:

    @staticmethod
    def flush():
        api_logging.pop_all()

    @staticmethod
    def commit_log():

        for request, response in api_logging.pop_all():
            try:
                attach_request(request)
            except Exception:
                pass
            try:
                attach_response(response)
                log_response(response)
            except Exception:
                pass

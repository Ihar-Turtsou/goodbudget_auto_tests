import allure
import logging

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)

logger.handlers.clear()

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
))
logger.addHandler(handler)

formatter = handler.formatter


def log_response(response):
    msg_plain = f"Response: {response.status_code} | URL: {response.url} | Size: {len(response.content)} bytes"

    logger.info(msg_plain)

    record = logging.LogRecord(
        name=logger.name,
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg=msg_plain,
        args=(),
        exc_info=None,
    )
    formatted_msg = formatter.format(record)

    allure.attach(
        formatted_msg,
        name="HTTP log",
        attachment_type=allure.attachment_type.TEXT,
    )

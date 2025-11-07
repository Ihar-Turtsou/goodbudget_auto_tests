import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def log_response(response):
    logger.info(
        f"Response: {response.status_code} | URL: {response.url} | Size: {len(response.content)} bytes"
    )

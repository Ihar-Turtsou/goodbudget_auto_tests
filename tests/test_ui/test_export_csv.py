import random

import allure
import pytest

from utils.api_helpers import (
    add_transactions_by_envelope_uuid,
    delete_transaction_by_uuid,
    get_envelope_uuid,
)
from utils.file_helpers import (
    assert_csv_contains,
    download_file_from_url,
    get_download_path,
)

# @pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.usefixtures("setup_browser")
@allure.label("layer", "UI Tests")
@allure.tag("web", "export")
@allure.feature("[WEB] Export CSV")
@allure.story("Export transactions to CSV")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://goodbudget.com/home", name="Export button location")
def test_export_csv_ui(transactions_manager, session_cookie, credentials, home_page):

    transaction = transactions_manager.create("Extra")

    home_page.open_home_with_cookie(session_cookie)
    download_url = home_page.get_export_csv_link()

    csv_path = get_download_path("history.csv")
    download_file_from_url(download_url, session_cookie, csv_path)
    assert_csv_contains(csv_path, transaction["transaction_name"])

    transactions_manager.delete(transaction_uuid=transaction["transaction_uuid"])

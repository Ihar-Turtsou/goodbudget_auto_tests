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

@pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
@allure.label("layer", "UI Tests")
@allure.tag("web", "export")
@allure.feature("[WEB] Export CSV")
@allure.story("Export transactions to CSV")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://goodbudget.com/home", name="Export button location")
def test_export_csv_ui(setup_browser, session_cookie, credentials, home_page):

    transaction_name = f"Export № {random.randint(500, 1000)}"

    envelope_uuid = get_envelope_uuid(session_cookie, credentials, "Extra")
    transaction_data = add_transactions_by_envelope_uuid(
        session_cookie, credentials, transaction_name, envelope_uuid
    )

    home_page.open_home_with_cookie(credentials, session_cookie)
    download_url = home_page.get_export_csv_link()

    csv_path = get_download_path("history.csv")
    download_file_from_url(download_url, session_cookie, csv_path)
    assert_csv_contains(csv_path, transaction_name)

    delete_transaction_by_uuid(session_cookie, credentials, transaction_data["uuid"])

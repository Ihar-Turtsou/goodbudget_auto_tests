from os import write

import pytest, random, requests, csv
from selene import have, browser, query
from utils.api_helpers import get_envelope_uuid, add_transactions_by_envelope_uuid

# @pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_export_csv_ui(setup_browser, browser_logged_in, session_cookie, credentials):

    transaction_name = f'Export № {random.randint(500, 1000)}'

    envelope_uuid =  get_envelope_uuid(session_cookie, credentials, 'Extra')
    add_transactions_by_envelope_uuid(session_cookie, credentials, transaction_name, envelope_uuid)

    download_url = browser.element('[id="export-txns"]').get(query.attribute("href"))

    content = requests.get(url=download_url, cookies={'GBSESS': session_cookie}).content

    with open("resources/downloads/history.csv", "wb") as file:
        file.write(content)

    transaction_name = '123'
    with open("resources/downloads/history.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        assert any(transaction_name in row for row in reader), f"Transaction '{transaction_name}' not found in exported CSV"
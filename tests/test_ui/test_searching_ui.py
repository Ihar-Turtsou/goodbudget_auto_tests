import pytest, random
from selene import have, browser
from utils.api_helpers import get_envelope_uuid, add_transactions_by_envelope_uuid

@pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_add_transaction_ui(setup_browser, browser_logged_in, session_cookie, credentials):

    transaction_name = f'Saving № {random.randint(0, 100)}'

    envelope_uuid =  get_envelope_uuid(session_cookie, credentials, 'Savings')
    add_transactions_by_envelope_uuid(session_cookie, credentials, transaction_name, envelope_uuid)

    browser.element('.ui-autocomplete-input').set_value(transaction_name)
    browser.element('[id="trans-search-btn"]').click()

    browser.all('[id="transactions-tbody"] .transaction .payee strong')[0].should(have.exact_text(transaction_name))




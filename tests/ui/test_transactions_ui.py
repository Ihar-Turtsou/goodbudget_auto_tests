from difflib import Match

import pytest,json, random
from selene import have, browser
import requests


from utils.api_helpers import get_envelope_uuid, get_transactions_by_uuid, add_transactions_by_envelope_uuid

@pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_add_transaction_ui(setup_browser, browser_logged_in,session_cookie, credentials):
    name_of_transaction = f'Payment for rent {random.randint(0, 100)}'
    envelope_uuid =  get_envelope_uuid(session_cookie, credentials, 'Groceries')
    browser.element('.addTransaction').click()
    browser.element('[id="expense-receiver"]').set_value(name_of_transaction)
    browser.element('[id = "expense-amount"]').set_value('150')
    browser.element(f'.controls.envelope [name="envelopeUuid"] [value="{envelope_uuid}"]').click()
    browser.element('[id="addTransactionSave"]').click()

    transactions = get_transactions_by_uuid(session_cookie,credentials,envelope_uuid)

    # print(json.dumps(transactions, indent=2, ensure_ascii=False))
    items = transactions.get('items', [])

    transaction_uuid = None
    for transaction in items:
        if transaction.get('receiver') == name_of_transaction:
            transaction_uuid = transaction.get('uuid')
            break


    # print(transaction_uuid)
    assert any(t.get('uuid') == transaction_uuid for t in items)


# python -m pytest -s
# @pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_edit_transaction_ui(setup_browser, browser_logged_in,session_cookie, credentials):
    envelope_uuid = get_envelope_uuid(session_cookie, credentials, 'Gas')
    # add_transactions_by_envelope_uuid(session_cookie, credentials, envelope_uuid)
    browser.all('[id="wrapper-envelopes"] .nodes .name').element_by(have.exact_text('Gas')).click()
    browser.all('[id="transactions-tbody"] .transaction .payee').element_by(have.text('Some API Transaction')).click()

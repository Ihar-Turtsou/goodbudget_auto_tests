import pytest, random
from selene import have, browser
from utils.api_helpers import get_envelope_uuid, get_transactions_by_envelope_uuid, add_transactions_by_envelope_uuid


@pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_add_transaction_ui(setup_browser, browser_logged_in,session_cookie, credentials):
    transaction_name = f'Payment for rent {random.randint(0, 100)}'
    transaction_amount = random.randint(10, 300)
    envelope_uuid =  get_envelope_uuid(session_cookie, credentials, 'Groceries')
    browser.element('.addTransaction').click()
    browser.element('[id="expense-receiver"]').set_value(transaction_name)
    browser.element('[id = "expense-amount"]').set_value(transaction_amount)
    browser.element(f'.controls.envelope [name="envelopeUuid"] [value="{envelope_uuid}"]').click()
    browser.element('[id="addTransactionSave"]').click()

    transactions = get_transactions_by_envelope_uuid(session_cookie, credentials, envelope_uuid)
    items = transactions.get('items', [])


    assert any(
        t.get('receiver') == transaction_name
        and t.get('amount') == f"{transaction_amount:.2f}"
        and t.get('envelope_uuid') == envelope_uuid
        for t in items
    ), f" Transaction '{transaction_name}' (amount={transaction_amount}) not found in envelope {envelope_uuid}"


@pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_edit_transaction_ui(setup_browser, browser_logged_in, session_cookie, credentials):
    envelope_uuid = get_envelope_uuid(session_cookie, credentials, 'Gas')
    transaction_name = 'Some payment for gas'
    transaction_data = add_transactions_by_envelope_uuid(session_cookie, credentials, transaction_name, envelope_uuid)

    transaction_name_edited = f'Payment for gas {random.randint(0, 100)}'
    transaction_amount_edited = random.randint(300, 900)

    browser.all('[id="wrapper-envelopes"] .nodes .name').element_by(have.exact_text('Gas')).click()
    browser.all('[id="transactions-tbody"] .transaction .payee').element_by(have.text(transaction_data['name'])).click()
    browser.element('[id="expense-receiver"]').set_value(transaction_name_edited)
    browser.element('[id = "expense-amount"]').set_value(transaction_amount_edited)
    browser.element(f'.controls.envelope [name="envelopeUuid"] [value="{envelope_uuid}"]').click()
    browser.element('[id="addTransactionSave"]').click()

    transactions = get_transactions_by_envelope_uuid(session_cookie, credentials, envelope_uuid)
    items = transactions.get('items', [])

    assert any(
        t.get('receiver') == transaction_name_edited
        and t.get('amount') == f"{transaction_amount_edited:.2f}"
        and t.get('envelope_uuid') == envelope_uuid
        for t in items
    ), f" Transaction '{transaction_name_edited}' (amount={transaction_amount_edited}) not found in envelope {envelope_uuid}"

@pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_delete_transaction_ui(setup_browser, browser_logged_in, session_cookie, credentials):
    envelope_uuid = get_envelope_uuid(session_cookie, credentials, 'Chemical')
    transaction_name = f'Payment for deletion {random.randint(0, 100)}'
    transaction_data = add_transactions_by_envelope_uuid(session_cookie, credentials, transaction_name, envelope_uuid)
    browser.all('[id="wrapper-envelopes"] .nodes .name').element_by(have.exact_text('Chemical')).click()
    browser.all('[id="transactions-tbody"] .transaction .payee').element_by(have.text(transaction_data['name'])).click()
    browser.element('[id="addTransactionDelete"]').click()

    transactions = get_transactions_by_envelope_uuid(session_cookie, credentials, envelope_uuid)
    items = transactions.get('items', [])

    assert all(t.get('uuid') != transaction_data['uuid'] for t in items)
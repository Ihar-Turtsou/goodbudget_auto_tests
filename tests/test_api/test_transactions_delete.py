import pytest, random, allure
from utils.api_helpers import (
    get_envelope_uuid,
    get_transactions_by_envelope_uuid,
    add_transactions_by_envelope_uuid,
    delete_transaction_by_uuid
)

# @pytest.mark.api
def test_delete_transaction_api(setup_browser, session_cookie, credentials):
    envelope_uuid = get_envelope_uuid(session_cookie,credentials,'API')
    transaction_name = f'API transaction deleted № {random.randint(0, 100)}'
    transaction_data = add_transactions_by_envelope_uuid(session_cookie,credentials,transaction_name,envelope_uuid)

    response = delete_transaction_by_uuid(session_cookie,credentials,transaction_data['uuid'])
    assert response.status_code == 200

    transactions = get_transactions_by_envelope_uuid(session_cookie,credentials,envelope_uuid)
    items = transactions.get('items', [])

    assert all(t.get('uuid') != transaction_data['uuid'] for t in items), "Transaction still present after delete"


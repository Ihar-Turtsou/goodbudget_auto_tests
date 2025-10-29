import pytest, random, allure
from utils.api_helpers import (
    get_envelope_uuid,
    get_transactions_by_envelope_uuid,
    add_transactions_by_envelope_uuid,
    delete_transaction_by_uuid
)
from utils.schema import validate_schema
from utils.logger_allure import  attach_response, attach_request
from utils.logger_console import log_response

@pytest.mark.api
@pytest.mark.regression
@allure.label("layer", "API Tests")
@allure.tag("api", "transactions")
@allure.feature("[API] Transactions API")
@allure.story("Delete new transaction via API")
@allure.severity(allure.severity_level.NORMAL)
@allure.link("https://goodbudget.com/api/transactions/save", name="POST /api/transactions/save")
def test_delete_transaction_api(session_cookie, credentials):

    with allure.step('Prepare test data'):
        envelope_name = 'Hobby'
        envelope_uuid = get_envelope_uuid(session_cookie,credentials,envelope_name)
        txn_name = f'API transaction deleted № {random.randint(0, 100)}'

    with allure.step('Send POST request to Create a transaction'):
        txn_data = add_transactions_by_envelope_uuid(session_cookie,credentials,txn_name,envelope_uuid)

    with allure.step('Send POST request to Delete a transaction'):
        del_txn_data = delete_transaction_by_uuid(session_cookie,credentials,txn_data['uuid'])
        attach_request(del_txn_data['del_request'])
        attach_response(del_txn_data['del_response'])
        log_response(del_txn_data['del_response'])


    with allure.step('Validate response structure and status code'):
        assert del_txn_data['del_response'].status_code == 200
        validate_schema(txn_data['response'].json(), "transaction_save_response.json")

    with allure.step('Verify transaction presence via GET /api/transactions'):
        txns = get_transactions_by_envelope_uuid(session_cookie,credentials,envelope_uuid)
        items = txns.json().get('items', [])
        assert all(t.get('uuid') != txn_data['uuid'] for t in items), "Transaction still present after delete"


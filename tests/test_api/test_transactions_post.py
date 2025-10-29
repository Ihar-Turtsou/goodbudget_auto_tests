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
@allure.story("Add new transaction via API")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://goodbudget.com/api/transactions/save", name="POST /api/transactions/save")
def test_add_transaction_api(session_cookie, credentials):

    with allure.step('Prepare test data'):
        envelope_name = 'Hobby'
        envelope_uuid = get_envelope_uuid(session_cookie,credentials,envelope_name)
        txn_name = f'API transaction created № {random.randint(0, 100)}'

    with allure.step('Send POST request to create a transaction'):
        txn_data = add_transactions_by_envelope_uuid(session_cookie,credentials,txn_name,envelope_uuid)
        attach_request(txn_data['request'])
        attach_response(txn_data['response'])
        log_response(txn_data['response'])

    with allure.step('Validate response structure and status code'):
        assert txn_data['response'].status_code == 200
        validate_schema(txn_data['response'].json(), "transaction_save_response.json" )

    with allure.step('Verify transaction presence via GET /api/transactions'):
        txns = get_transactions_by_envelope_uuid(session_cookie,credentials,envelope_uuid)
        items = txns.json().get('items', [])
        assert any(
            t.get('receiver') == txn_name
            and t.get('envelope_uuid') == envelope_uuid
            for t in items
        ), f" Transaction '{txn_name}' not found in envelope {envelope_uuid}"

    with allure.step('Cleanup - delete created transaction'):
        delete_transaction_by_uuid(session_cookie,credentials,txn_data['uuid'])
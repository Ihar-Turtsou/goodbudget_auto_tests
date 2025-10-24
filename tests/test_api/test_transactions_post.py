import pytest, random, allure
from utils.api_helpers import (
    get_envelope_uuid,
    get_transactions_by_envelope_uuid,
    add_transactions_by_envelope_uuid,
    delete_transaction_by_uuid
)
from utils.schema import validate_schema

@pytest.mark.api
@pytest.mark.regression
@allure.tag("api", "transactions")
@allure.feature("Transactions API")
@allure.story("Add new transaction via API")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://goodbudget.com/api/transactions/save", name="POST /api/transactions/save")
def test_add_transaction_api(setup_browser, session_cookie, credentials):

    with allure.step('Prepare test data'):
        envelope_uuid = get_envelope_uuid(session_cookie,credentials,'API')
        transaction_name = f'API transaction created № {random.randint(0, 100)}'

    with allure.step('Send POST request to create a transaction'):
        transaction_data = add_transactions_by_envelope_uuid(session_cookie,credentials,transaction_name,envelope_uuid)

    with allure.step('Validate response structure and status code'):
        assert transaction_data['response'].status_code == 200
        validate_schema(transaction_data['response'].json(), "transaction_save_response.json" )

    with allure.step('Verify transaction presence via GET /api/transactions'):
        transactions = get_transactions_by_envelope_uuid(session_cookie,credentials,envelope_uuid)
        items = transactions.get('items', [])
        assert any(
            t.get('receiver') == transaction_name
            and t.get('envelope_uuid') == envelope_uuid
            for t in items
        ), f" Transaction '{transaction_name}' not found in envelope {envelope_uuid}"

    with allure.step('Cleanup - delete created transaction'):
        delete_transaction_by_uuid(session_cookie,credentials,transaction_data['uuid'])
import pytest, random, allure
from utils.api_helpers import (
    get_envelope_uuid,
    add_transactions_by_envelope_uuid,
    get_existing_transaction_data,
    delete_transaction_by_uuid,get_transactions_by_envelope_uuid,get_all_envelopes
)
from utils.schema import validate_schema
from utils.logger_allure import  attach_response, attach_request
from utils.logger_console import log_response

@pytest.mark.api
@pytest.mark.regression
@allure.tag("api", "transactions")
@allure.feature("Transactions API")
@allure.story("Get transaction by UUID via API")
@allure.severity(allure.severity_level.NORMAL)
@allure.link("https://goodbudget.com/api/transactions/get/uuid", name="GET /api/transactions/get/uuid")
def test_get_txn_api(setup_browser, session_cookie, credentials):

    with allure.step('Prepare test data'):
        envelope_name = 'Hobby'
        envelope_uuid = get_envelope_uuid(session_cookie,credentials,envelope_name)
        txn_name = f'API transaction for check № {random.randint(0, 100)}'

    with allure.step('Create a transaction'):
        txn_data = add_transactions_by_envelope_uuid(session_cookie,credentials,txn_name,envelope_uuid)

    with allure.step('GET created transaction by UUID'):
        get_txn_data = get_existing_transaction_data(txn_data["uuid"],credentials, session_cookie)
        attach_response(get_txn_data)
        log_response(get_txn_data)

    with allure.step('Validate response structure and status code'):
        assert get_txn_data.status_code == 200
        validate_schema(get_txn_data.json(), "transaction_get_response.json")

    with allure.step('Cleanup - delete created transaction'):
        delete_transaction_by_uuid(session_cookie, credentials, txn_data['uuid'])


@pytest.mark.api
@pytest.mark.regression
@allure.tag("api", "transactions")
@allure.feature("Transactions API")
@allure.story("List transactions by envelope")
@allure.severity(allure.severity_level.NORMAL)
@allure.link("https://goodbudget.com/api/transactions", name="GET /api/transactions")
def test_get_txns_by_envelope_api(setup_browser, session_cookie, credentials):

    with allure.step('Prepare test data'):
        envelope_name = 'Hobby'
        envelope_uuid = get_envelope_uuid(session_cookie,credentials, envelope_name)
        txn_name = f'API transaction for check Envelope №{random.randint(0, 100)}'

    with allure.step(f'Create a transaction in {envelope_name}'):
        txn_data = add_transactions_by_envelope_uuid(session_cookie,credentials,txn_name,envelope_uuid)

    with allure.step(f'GET transactions list {envelope_name}'):
        get_txns_envelope = get_transactions_by_envelope_uuid(session_cookie, credentials, envelope_uuid)
        attach_response(get_txns_envelope)
        log_response(get_txns_envelope)

    with allure.step('Validate response structure and status code'):
        assert get_txns_envelope.status_code == 200
        validate_schema(get_txns_envelope.json(), "envelope_transactions_list_response.json")

    with allure.step('Cleanup - delete created transaction'):
        delete_transaction_by_uuid(session_cookie, credentials, txn_data['uuid'])



@pytest.mark.api
@pytest.mark.regression
@allure.tag("api", "envelopes")
@allure.feature("Envelopes API")
@allure.story("Get all envelopes")
@allure.severity(allure.severity_level.NORMAL)
@allure.link("https://goodbudget.com/api/envelopes", name="GET /api/envelopes")
def test_get_all_envelopes_api(setup_browser, session_cookie, credentials):

    with allure.step('Prepare test data'):
        envelope_name = 'Hobby'
        envelope_uuid = get_envelope_uuid(session_cookie,credentials, envelope_name)
        txn_name = f'API transaction for check Envelope №{random.randint(0, 100)}'

    with allure.step(f"Create a transaction in envelope '{envelope_name}'"):
        txn_data = add_transactions_by_envelope_uuid(session_cookie,credentials,txn_name,envelope_uuid)

    with allure.step('Get all Envelopes'):
        envelope = get_all_envelopes(session_cookie,credentials)
        attach_response(envelope)
        log_response(envelope)

    with allure.step('Validate response status and JSON schema'):
        assert envelope.status_code == 200
        validate_schema(envelope.json(), "envelopes_response.json")

    with allure.step('Cleanup - delete created transaction'):
        delete_transaction_by_uuid(session_cookie, credentials, txn_data['uuid'])

import random

import allure
import pytest

from utils.api_helpers import (
    get_existing_transaction_data,
    get_transactions_by_envelope_uuid,
)
from utils.logger_allure import attach_response
from utils.logger_console import log_response
from utils.schema import validate_schema


# @pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.api
@pytest.mark.regression
@allure.label("layer", "API Tests")
@allure.tag("api", "transactions")
@allure.feature("[API] Transactions API")
class TestTransactionsGet:

    # @pytest.mark.skip(reason="This test is temporarily disabled.")
    @allure.story("Get transaction by UUID via API")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://goodbudget.com/api/transactions/get/uuid", name="GET /api/transactions/get/uuid")
    def test_get_txn_api(self, api_logger, api_steps, session_cookie, transactions_manager, credentials):

        txn = transactions_manager.create("Hobby")

        response = api_steps.get_txn_data(txn["transaction_uuid"], credentials, session_cookie)
        api_logger.commit_log()

        api_steps.validate_schema(response, "transaction_get_response.json")

        transactions_manager.delete(txn["transaction_uuid"])

    # @pytest.mark.skip(reason="This test is temporarily disabled.")
    @allure.story("List transactions by envelope")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://goodbudget.com/api/transactions", name="GET /api/transactions")
    def test_get_txns_by_envelope_api(self, api_logger, api_steps, session_cookie, transactions_manager, credentials):

        txn = transactions_manager.create("Hobby")

        response  = api_steps.get_envelope_data(session_cookie, credentials, txn["envelope_uuid"])
        api_logger.commit_log()

        api_steps.validate_schema(response["response"], "envelope_transactions_list_response.json")
        transactions_manager.delete(txn["transaction_uuid"])




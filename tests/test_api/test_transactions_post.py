import random

import allure
import pytest

from utils.api_helpers import (
    get_transactions_by_envelope_uuid,
)

from utils.schema import validate_schema

# @pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.api
@pytest.mark.regression
@allure.label("layer", "API Tests")
@allure.tag("api", "transactions")
@allure.feature("[API] Transactions API")
@allure.story("Add new transaction via API")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(
    "https://goodbudget.com/api/transactions/save", name="POST /api/transactions/save"
)
def test_add_transaction_api(api_logger, api_steps, session_cookie, transactions_manager, credentials):

    txn = transactions_manager.create("Hobby")
    api_logger.commit_log()
    api_steps.validate_schema(txn["response"],"transaction_save_response.json")
    api_steps.assert_transaction_present(session_cookie, credentials, txn["envelope_uuid"], txn["transaction_name"])

    transactions_manager.delete(transaction_uuid=txn["transaction_uuid"])

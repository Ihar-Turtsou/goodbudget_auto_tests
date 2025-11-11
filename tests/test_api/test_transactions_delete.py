import allure
import pytest


@pytest.mark.api
@pytest.mark.regression
@allure.label("layer", "API Tests")
@allure.tag("api", "transactions")
@allure.feature("[API] Transactions API")
@allure.story("Delete new transaction via API")
@allure.severity(allure.severity_level.NORMAL)
@allure.link(
    "https://goodbudget.com/api/transactions/save", name="POST /api/transactions/save"
)
def test_delete_transaction_api(
    api_logger, api_steps, session_cookie, transactions_manager, credentials
):

    txn = transactions_manager.create("Hobby")

    txn_deleted = transactions_manager.delete(txn["transaction_uuid"])
    api_logger.commit_log()
    api_steps.validate_schema(txn_deleted["del_response"], "transaction_save_response.json")
    api_steps.assert_transaction_not_present(
        session_cookie, credentials, txn["envelope_uuid"], txn["transaction_uuid"]
    )

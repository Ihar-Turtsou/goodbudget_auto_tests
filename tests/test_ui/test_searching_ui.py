import allure
import pytest


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.usefixtures("setup_browser")
@allure.label("layer", "UI Tests")
@allure.tag("web", "search")
@allure.feature("[WEB] Transactions")
@allure.story("Search transaction on Home (UI)")
@allure.severity(allure.severity_level.NORMAL)
@allure.link("https://goodbudget.com/home", name="Home")
def test_transaction_searching_ui(
    transactions_manager, session_cookie, credentials, home_page
):

    transaction = transactions_manager.create("Savings")

    (
        home_page.open_home_with_cookie(session_cookie)
        .set_search_query(transaction["transaction_name"])
        .submit_search()
        .searching_result_should_be(transaction["transaction_name"])
    )

    transactions_manager.delete(transaction_uuid=transaction["transaction_uuid"])

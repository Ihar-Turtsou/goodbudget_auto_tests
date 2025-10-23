import pytest, random, allure
from utils.api_helpers import (
    get_envelope_uuid,
    add_transactions_by_envelope_uuid,
    delete_transaction_by_uuid
)


@pytest.mark.ui
@pytest.mark.regression
@allure.tag("web", "search")
@allure.feature("Transactions")
@allure.story("Search transactions (UI)")
@allure.severity(allure.severity_level.NORMAL)
@allure.link("https://goodbudget.com/home", name="Home")
def test_transaction_searching_ui(
        setup_browser,
        session_cookie,
        credentials,
        home_page
):

    transaction_name = f'Saving № {random.randint(2000, 3000)}'
    envelope_uuid =  get_envelope_uuid(
        session_cookie,
        credentials,
        'Savings')
    transaction_data = add_transactions_by_envelope_uuid(
        session_cookie,
        credentials,
        transaction_name,
        envelope_uuid
    )

    (
        home_page
        .open_home_with_cookie(credentials, session_cookie)
        .set_search_query(transaction_name)
        .submit_search()
        .searching_result_should_be(transaction_name)
    )

    delete_transaction_by_uuid(
        session_cookie,
        credentials,
        transaction_data['uuid']
    )






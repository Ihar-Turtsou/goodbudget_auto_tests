import random

import allure
import pytest

from utils.api_helpers import get_envelope_uuid, get_transactions_by_envelope_uuid


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.usefixtures("setup_browser")
@allure.label("layer", "UI Tests")
@allure.tag("web", "transactions")
@allure.feature("[WEB] Manage transactions")
@allure.link("https://goodbudget.com/home", name="Home")
class TestTransactionUi:

    @pytest.mark.smoke
    @allure.story("Add transaction on Home (UI+API verify)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_transaction_ui(
        self, transactions_manager, session_cookie, credentials, home_page
    ):
        transaction_name = f"Payment for rent {random.randint(0, 100)}"
        transaction_amount = random.randint(10, 300)
        envelope_uuid = get_envelope_uuid(session_cookie, credentials, "Groceries")
        (
            home_page.open_home_with_cookie(session_cookie)
            .add_transaction()
            .fill_transaction_name(transaction_name)
            .fill_transaction_amount(transaction_amount)
            .set_transaction_envelope(envelope_uuid)
            .save_transaction()
        )

        transactions = get_transactions_by_envelope_uuid(
            session_cookie, credentials, envelope_uuid
        )
        assert any(
            t.get("receiver") == transaction_name
            and t.get("amount") == f"{transaction_amount:.2f}"
            and t.get("envelope_uuid") == envelope_uuid
            for t in transactions["items"]
        ), f" Transaction '{transaction_name}' (amount={transaction_amount}) not found in envelope {envelope_uuid}"

        transactions_manager.delete(
            transaction_name=transaction_name,
            envelope_transactions=transactions["items"],
        )

    @allure.story("Edit transaction on Home (UI+API verify)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_transaction_ui(
        self, transactions_manager, session_cookie, credentials, home_page
    ):

        transaction = transactions_manager.create("Gas")
        transaction_name_edited = f"Payment for gas {random.randint(0, 100)}"
        transaction_amount_edited = random.randint(300, 900)
        (
            home_page.open_home_with_cookie(session_cookie)
            .choose_envelope("Gas")
            .edit_transaction(transaction["transaction_name"])
            .fill_transaction_name(transaction_name_edited)
            .fill_transaction_amount(transaction_amount_edited)
            .set_transaction_envelope(transaction["envelope_uuid"])
            .save_transaction()
        )

        transactions = get_transactions_by_envelope_uuid(
            session_cookie, credentials, transaction["envelope_uuid"]
        )
        assert any(
            t.get("receiver") == transaction_name_edited
            and t.get("amount") == f"{transaction_amount_edited:.2f}"
            and t.get("envelope_uuid") == transaction["envelope_uuid"]
            for t in transactions["items"]
        ), f" Transaction '{transaction_name_edited}' (amount={transaction_amount_edited}) not found in envelope {transaction["envelope_uuid"]}"

        transactions_manager.delete(transaction_uuid=transaction["transaction_uuid"])

    @allure.story("Delete transaction from Home (UI+API verify)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_transaction_ui(
        self, transactions_manager, session_cookie, credentials, home_page
    ):

        transaction = transactions_manager.create("Chemical")
        (
            home_page.open_home_with_cookie(session_cookie)
            .choose_envelope("Chemical")
            .edit_transaction(transaction["transaction_name"])
            .delete_transaction_ui()
        )
        transactions = get_transactions_by_envelope_uuid(
            session_cookie, credentials, transaction["envelope_uuid"]
        )

        assert all(
            t.get("uuid") != transaction["transaction_uuid"]
            for t in transactions["items"]
        ), "Transaction still present after delete"

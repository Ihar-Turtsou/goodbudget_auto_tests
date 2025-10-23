import pytest, random, allure
from utils.api_helpers import (
    get_envelope_uuid,
    get_transactions_by_envelope_uuid,
    add_transactions_by_envelope_uuid,
    delete_transaction_by_uuid
)

@pytest.mark.ui
@pytest.mark.regression
@allure.tag("web", "transactions")
@allure.feature("Transactions")
@allure.link("https://goodbudget.com/home", name="Home")
class TestTransactionUi:

    @pytest.mark.smoke
    @allure.story("Add transaction (UI+API verify)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_transaction_ui(self,
            setup_browser,
            session_cookie,
            credentials,
            home_page):
        transaction_name = f'Payment for rent {random.randint(0, 100)}'
        transaction_amount = random.randint(10, 300)
        envelope_uuid =  get_envelope_uuid(
            session_cookie,
            credentials,
            'Groceries'
        )

        (
            home_page
            .open_home_with_cookie(credentials, session_cookie)
            .add_transaction()
            .fill_transaction_name(transaction_name)
            .fill_transaction_amount(transaction_amount)
            .set_transaction_envelope(envelope_uuid)
            .save_transaction()
         )

        transactions = get_transactions_by_envelope_uuid(
            session_cookie,
            credentials,
            envelope_uuid
        )
        items = transactions.get('items', [])

        assert any(
            t.get('receiver') == transaction_name
            and t.get('amount') == f"{transaction_amount:.2f}"
            and t.get('envelope_uuid') == envelope_uuid
            for t in items
        ), f" Transaction '{transaction_name}' (amount={transaction_amount}) not found in envelope {envelope_uuid}"

        transaction_data = next((t for t in items if t.get('receiver') == transaction_name), None)
        delete_transaction_by_uuid(
            session_cookie,
            credentials,
            transaction_data['uuid']
        )


    @allure.story("Edit transaction (UI+API verify)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_transaction_ui(self,
            setup_browser,
            session_cookie,
            credentials,
            home_page
    ):
        envelope_uuid = get_envelope_uuid(
            session_cookie,
            credentials,
            'Gas')
        transaction_name = 'Some payment for gas'
        transaction_data = add_transactions_by_envelope_uuid(
            session_cookie,
            credentials,
            transaction_name,
            envelope_uuid
        )
        transaction_name_edited = f'Payment for gas {random.randint(0, 100)}'
        transaction_amount_edited = random.randint(300, 900)

        (
            home_page
            .open_home_with_cookie(credentials, session_cookie)
            .choose_envelope('Gas')
            .edit_transaction(transaction_data['name'])
            .fill_transaction_name(transaction_name_edited)
            .fill_transaction_amount(transaction_amount_edited)
            .set_transaction_envelope(envelope_uuid)
            .save_transaction()
        )

        transactions = get_transactions_by_envelope_uuid(
            session_cookie,
            credentials,
            envelope_uuid
        )
        items = transactions.get('items', [])

        assert any(
            t.get('receiver') == transaction_name_edited
            and t.get('amount') == f"{transaction_amount_edited:.2f}"
            and t.get('envelope_uuid') == envelope_uuid
            for t in items
        ), f" Transaction '{transaction_name_edited}' (amount={transaction_amount_edited}) not found in envelope {envelope_uuid}"

        delete_transaction_by_uuid(
            session_cookie,
            credentials,
            transaction_data['uuid']
        )




    @allure.story("Delete transaction (UI+API verify)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_transaction_ui(self,
            setup_browser,
            session_cookie,
            credentials,
            home_page
    ):
        envelope_uuid = get_envelope_uuid(
            session_cookie,
            credentials,
            'Chemical'
        )
        transaction_name = f'Payment for deletion {random.randint(0, 100)}'
        transaction_data = add_transactions_by_envelope_uuid(
            session_cookie,
            credentials,
            transaction_name,
            envelope_uuid
        )

        (
            home_page
            .open_home_with_cookie(credentials, session_cookie)
            .choose_envelope('Chemical')
            .edit_transaction(transaction_data['name'])
            .delete_transaction()
        )

        transactions = get_transactions_by_envelope_uuid(
            session_cookie,
            credentials,
            envelope_uuid
        )
        items = transactions.get('items', [])

        assert all(t.get('uuid') != transaction_data['uuid'] for t in items)

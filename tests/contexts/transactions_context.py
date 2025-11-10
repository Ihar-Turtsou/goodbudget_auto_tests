import random

import allure

from utils.api_helpers import (
    add_transactions_by_envelope_uuid,
    delete_transaction_by_uuid,
    get_envelope_uuid,
)


class TransactionsContext:
    def __init__(self, session_cookie, credentials):
        self.session_cookie = session_cookie
        self.credentials = credentials

    @allure.step("Create a transaction in envelope '{envelope_name}'")
    def create(self, envelope_name):
        envelope_uuid = get_envelope_uuid(
            self.session_cookie, self.credentials, envelope_name
        )
        transaction_name = (
            f"Test payment for {envelope_name} {random.randint(10, 10000)}"
        )
        transaction = add_transactions_by_envelope_uuid(
            self.session_cookie, self.credentials, transaction_name, envelope_uuid
        )
        return {
            "envelope_name": envelope_name,
            "envelope_uuid": envelope_uuid,
            "transaction_name": transaction["name"],
            "transaction_uuid": transaction["uuid"],
            "request": transaction["request"],
            "response": transaction["response"],
        }

    @allure.step("Delete a transaction ")
    def delete(
        self, transaction_uuid=None, transaction_name=None, envelope_transactions=None
    ):
        if transaction_uuid:
            delete_transaction_by_uuid(
                self.session_cookie, self.credentials, transaction_uuid
            )
            return
        else:
            transaction_data = next(
                (
                    t
                    for t in envelope_transactions
                    if t.get("receiver") == transaction_name
                ),
                None,
            )
            delete_transaction_by_uuid(
                self.session_cookie, self.credentials, transaction_data["uuid"]
            )

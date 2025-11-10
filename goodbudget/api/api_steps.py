import allure

from utils.api_helpers import (
    get_all_envelopes,
    get_existing_transaction_data,
    get_transactions_by_envelope_uuid,
)
from utils.schema import validate_schema


class ApiSteps:

    @allure.step("Validate response structure")
    def validate_schema(self, response, schema_file):
        validate_schema(response.json(), schema_file)
        return self

    @allure.step("Verify transaction presence via GET")
    def assert_transaction_present(
        self, session_cookie, credentials, envelope_uuid, txn_name
    ):
        txns = get_transactions_by_envelope_uuid(
            session_cookie, credentials, envelope_uuid
        )

        assert any(
            t.get("receiver") == txn_name and t.get("envelope_uuid") == envelope_uuid
            for t in txns["items"]
        ), f" Transaction '{txn_name}' not found in envelope"
        return self

    @allure.step("Verify transaction not presence via GET")
    def assert_transaction_not_present(
        self, session_cookie, credentials, envelope_uuid, txn_uuid
    ):
        txns = get_transactions_by_envelope_uuid(
            session_cookie,
            credentials,
            envelope_uuid,
        )

        assert all(
            t.get("uuid") != txn_uuid for t in txns["items"]
        ), "Transaction still present after delete"

        return self

    @allure.step("GET created transaction by UUID")
    def get_txn_data(self, transaction_uuid, credentials, session_cookie):
        response = get_existing_transaction_data(
            transaction_uuid, credentials, session_cookie
        )
        return response

    @allure.step("GET created transactions list")
    def get_envelope_data(self, session_cookie, credentials, envelope_uuid):
        response = get_transactions_by_envelope_uuid(
            session_cookie, credentials, envelope_uuid
        )
        return response

    @allure.step("Get all Envelopes")
    def get_all_envelopes_data(self, session_cookie, credentials):
        response = get_all_envelopes(session_cookie, credentials)
        return response

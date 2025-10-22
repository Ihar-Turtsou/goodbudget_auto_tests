from selene import have, browser

class HomePage:

    def open_home_with_temp_cookie(self, credentials, temp_cookie):
        browser.open("/")
        browser.driver.add_cookie({"name": "GBSESS", "value": temp_cookie})
        browser.open(f'{credentials["base_url"]}/home')
        return self

    def user_greeting_should_be(self, username):
        browser.element('[id="hi"]').should(have.text(username))
        return self

    def logout_from_account(self):
        browser.element('a[href="/logout"]').click()
        return self

    def set_search_query(self,transaction_name):
        browser.element('.ui-autocomplete-input').set_value(transaction_name)
        return self

    def submit_search(self):
        browser.element('[id="trans-search-btn"]').click()
        return self

    def searching_result_should_be(self, transaction_name):
        browser.all('[id="transactions-tbody"] .transaction .payee strong')[0].should(have.exact_text(transaction_name))
        return self

    def add_transaction(self):
        browser.element('.addTransaction').click()
        return self

    def fill_transaction_name(self, transaction_name):
        browser.element('[id="expense-receiver"]').set_value(transaction_name)
        return self

    def fill_transaction_amount(self, transaction_amount):
        browser.element('[id = "expense-amount"]').set_value(transaction_amount)
        return self

    def set_transaction_envelope(self, envelope_uuid):
        browser.element(f'.controls.envelope [name="envelopeUuid"] [value="{envelope_uuid}"]').click()
        return self

    def save_transaction(self):
        browser.element('[id="addTransactionSave"]').click()
        return self

    def choose_envelope(self, envelope_name):
        browser.all('[id="wrapper-envelopes"] .nodes .name').element_by(have.exact_text(envelope_name)).click()
        return self

    def edit_transaction(self, transaction_name):
        browser.all('[id="transactions-tbody"] .transaction .payee').element_by(
            have.text(transaction_name)).click()
        return self

    def delete_transaction(self):
        browser.element('[id="addTransactionDelete"]').click()
        return self
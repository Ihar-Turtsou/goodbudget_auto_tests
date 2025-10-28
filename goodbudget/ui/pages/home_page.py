from selene import have, browser, query, be
import allure

class HomePage:

    @allure.step('Open Home page using provided session cookie')
    def open_home_with_cookie(self, credentials, cookie_value):
        browser.open("/")
        browser.driver.add_cookie({
            "name": "GBSESS",
            "value": cookie_value,
            "path": "/",
        })
        browser.open(f'{credentials["base_url"]}/home')
        return self


    @allure.step('Get Export CSV link (href)')
    def get_export_csv_link(self):
        return browser.element('[id="export-txns"]').get(query.attribute("href"))


    @allure.step('Verify user greeting is displayed for "{username}"')
    def user_greeting_should_be(self, username):
        browser.element('[id="hi"]').should(have.text(username))
        return self


    @allure.step('Log out from account')
    def logout_from_account(self):
        browser.element('a[href="/logout"]').click()
        return self


    @allure.step("Enter '{transaction_name}' into search input")
    def set_search_query(self,transaction_name):
        browser.element('.ui-autocomplete-input').click().type(transaction_name)
        return self


    @allure.step('Submit search request')
    def submit_search(self):
        browser.element('[id="trans-search-btn"]').click()
        return self


    @allure.step("Verify search results contain transaction '{transaction_name}'")
    def searching_result_should_be(self, transaction_name):
        browser.all('[id="transactions-tbody"] .transaction .payee strong')[0].should(have.exact_text(transaction_name))
        return self


    @allure.step("Click 'Add Transaction' button")
    def add_transaction(self):
        browser.element('.addTransaction').click()
        return self


    @allure.step("Fill transaction name: '{transaction_name}'")
    def fill_transaction_name(self, transaction_name):
        browser.element('[id="expense-receiver"]').should(be.visible).click().type(transaction_name)
        return self


    @allure.step("Fill transaction amount: '{transaction_amount}'")
    def fill_transaction_amount(self, transaction_amount):
        browser.element('[id = "expense-amount"]').should(be.visible).click().type(transaction_amount)
        return self


    @allure.step("Select envelope by UUID")
    def set_transaction_envelope(self, envelope_uuid):
        browser.element(f'.controls.envelope [name="envelopeUuid"] [value="{envelope_uuid}"]').click()
        return self


    @allure.step("Save transaction")
    def save_transaction(self):
        browser.element('[id="addTransactionSave"]').click()
        return self


    @allure.step("Open envelope '{envelope_name}'")
    def choose_envelope(self, envelope_name):
        browser.all('[id="wrapper-envelopes"] .nodes .name').element_by(have.exact_text(envelope_name)).click()
        return self


    @allure.step("Edit transaction '{transaction_name}'")
    def edit_transaction(self, transaction_name):
        browser.all('[id="transactions-tbody"] .transaction .payee').element_by(
            have.text(transaction_name)).click()
        return self


    @allure.step("Delete selected transaction")
    def delete_transaction(self):
        browser.element('[id="addTransactionDelete"]').click()
        return self
from selene import have, browser

class HomePage:


    def user_greeting_should_be(self, username):
        browser.element('[id="hi"]').should(have.text(username))
        return self

    def logout_from_account(self):
        browser.element('a[href="/logout"]').click()
        return self

    def search_in_all_transactions(self,transaction_name):
        browser.element('.ui-autocomplete-input').set_value(transaction_name)
        browser.element('[id="trans-search-btn"]').click()
        return self

    def searching_result_should_be(self, transaction_name):
        browser.all('[id="transactions-tbody"] .transaction .payee strong')[0].should(have.exact_text(transaction_name))
        return self
from selene import have, browser

class HomePage:

    def user_greeting_should_be(self, username):
        browser.element('[id="hi"]').should(have.text(username))
        return self

    def logout_from_account(self):
        browser.element('a[href="/logout"]').click()
        return self
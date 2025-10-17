from selene import have, browser

class LoginPage:

    def open(self):
        browser.open('/login')
        return self

    def fill_username(self, username):
        browser.element('[id="username"]').set_value(username)
        return self

    def fill_password(self, password):
        browser.element('[id="password"]').set_value(password)
        return self

    def submit_form(self):
        browser.element('form[action="/login_check"]').submit()
        return self
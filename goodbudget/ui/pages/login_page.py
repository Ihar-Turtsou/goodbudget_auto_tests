from selene import browser
import allure

class LoginPage:

    @allure.step("Open login page")
    def open(self):
        browser.open('/login')
        return self

    @allure.step("Enter username: '{username}'")
    def fill_username(self, username):
        browser.element('[id="username"]').set_value(username)
        return self

    @allure.step("Enter password")
    def fill_password(self, password):
        browser.element('[id="password"]').set_value(password)
        return self

    @allure.step("Submit login form")
    def submit_form(self):
        browser.element('form[action="/login_check"]').submit()
        return self
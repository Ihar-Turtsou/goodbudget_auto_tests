import allure
from selene import browser, have, be
from appium.webdriver.common.appiumby import AppiumBy


class LoginScreen:

    LOGIN_ENTRY = (AppiumBy.ID, "com.dayspringtech.envelopes:id/login")
    FIELD_NAME = (AppiumBy.ID, "com.dayspringtech.envelopes:id/login_household_name")
    FIELD_PASSWORD  = (AppiumBy.ID, "com.dayspringtech.envelopes:id/login_password")
    BUTTON_SUBMIT   = (AppiumBy.ID, "com.dayspringtech.envelopes:id/login_button")
    CREATE_NEW_HH = (AppiumBy.ID, "com.dayspringtech.envelopes:id/register")


    @allure.step('Open Login form')
    def tap_login_entry(self):
        browser.element(self.LOGIN_ENTRY).click()
        return self

    @allure.step('Create new household account')
    def create_new_account(self):
        browser.element(self.CREATE_NEW_HH).click()
        return self

    @allure.step('Type name: {name}')
    def type_name(self, name):
        browser.element(self.FIELD_NAME).should(be.visible).type(name)
        return self

    @allure.step('Type password')
    def type_password(self, password):
        browser.element(self.FIELD_PASSWORD).should(be.visible).type(password)
        return self

    @allure.step('Submit form')
    def submit(self):
        browser.element(self.BUTTON_SUBMIT).click()
        return self
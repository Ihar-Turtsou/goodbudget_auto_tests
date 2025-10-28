import allure
from selene import browser
from appium.webdriver.common.appiumby import AppiumBy

class OnboardingScreen:


    SETUP_BUDGET = (AppiumBy.ID, "com.dayspringtech.envelopes:id/setup_budget_save_button")
    CONF_BUTTON = (AppiumBy.ID, "android:id/button1")
    LATER_BUTTON = (AppiumBy.ID, "com.dayspringtech.envelopes:id/later")

    @allure.step('Setup default budget')
    def setup_budget_next(self):
        browser.element(self.SETUP_BUDGET).click()
        return self

    @allure.step('Confirm modal popup')
    def confirm_modal(self):
        browser.element(self.CONF_BUTTON).click()
        return self

    @allure.step('Setup default budget later')
    def setup_budget_later(self):
        browser.element(self.LATER_BUTTON).click()
        return self
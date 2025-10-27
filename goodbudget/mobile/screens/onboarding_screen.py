import allure
from selene import browser, have, be
from appium.webdriver.common.appiumby import AppiumBy

class OnboardingScreen:


    LOGIN_ENTRY = (AppiumBy.ID, "com.dayspringtech.envelopes:id/login")
    FIELD_NAME = (AppiumBy.ID, "com.dayspringtech.envelopes:id/login_household_name")
    FIELD_PASSWORD = (AppiumBy.ID, "com.dayspringtech.envelopes:id/login_password")
    BUTTON_SUBMIT = (AppiumBy.ID, "com.dayspringtech.envelopes:id/login_button")
    CREATE_NEW_HH = (AppiumBy.ID, "com.dayspringtech.envelopes:id/register")


    browser.element('//android.widget.Button[@resource-id="com.dayspringtech.envelopes:id/setup_budget_save_button"]').click()
    browser.element('//android.widget.Button[@resource-id="android:id/button1"]').click()
    browser.element('//android.widget.Button[@resource-id="com.dayspringtech.envelopes:id/later"]').click()
    browser.element('//android.widget.Button[@resource-id="android:id/button1"]').click()



    def some(self):
        pass
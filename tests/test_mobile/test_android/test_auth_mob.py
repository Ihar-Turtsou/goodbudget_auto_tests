import pytest
from selene import browser, have, be


# @pytest.mark.mobile
def test_login_android_success(mobile_driver, credentials, login_screen, base_screen):
    browser.config.driver = mobile_driver

    (
        login_screen
        .tap_login_entry()
        .type_name("")
        .type_password("")
        .submit()
    )
    base_screen.should_see_toast('Login Successful')



# @pytest.mark.mobile
def test_login_android_fail(mobile_driver, login_screen, base_screen):
    browser.config.driver = mobile_driver
    (
        login_screen
        .tap_login_entry()
        .type_name("fdgdhthtere")
        .type_password("643xretv2kHerr")
        .submit()
    )
    base_screen.should_see_toast('Login failed. Please try again.')


@pytest.mark.mobile
def test_create_unregistered_account(mobile_driver, login_screen, home_screen):
    browser.config.driver = mobile_driver

    login_screen.create_new_account()


    browser.element('//android.widget.Button[@resource-id="com.dayspringtech.envelopes:id/setup_budget_save_button"]').click()
    browser.element('//android.widget.Button[@resource-id="android:id/button1"]').click()
    browser.element('//android.widget.Button[@resource-id="com.dayspringtech.envelopes:id/later"]').click()
    browser.element('//android.widget.Button[@resource-id="android:id/button1"]').click()
    home_screen.should_see_username('Unregistered')


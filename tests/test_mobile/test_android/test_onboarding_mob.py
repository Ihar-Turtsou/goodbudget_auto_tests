import pytest, allure
from selene import browser

@pytest.mark.mobile
@pytest.mark.regression
@allure.tag("mobile", "onboarding")
@allure.feature("Onboarding")
@allure.story("Create new unregistered account and complete onboarding")
@allure.severity(allure.severity_level.NORMAL)
@allure.link("https://goodbudget.com/signup", name="Create account screen")
@allure.description("Checks the creation of an unregistered (guest) account and the completion of onboarding.")
def test_create_unregistered_account(mobile_driver, login_screen, onboarding_screen, home_screen):
    browser.config.driver = mobile_driver
    login_screen.create_new_account()
    (
        onboarding_screen
        .setup_budget_next()
        .confirm_modal()
        .setup_budget_later()
        .confirm_modal()
    )

    home_screen.should_see_username('Unregistered')
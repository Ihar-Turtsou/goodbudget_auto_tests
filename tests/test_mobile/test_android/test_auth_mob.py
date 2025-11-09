import allure
import pytest
from selene import browser

@pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.mobile
@pytest.mark.regression
@allure.label("layer", "MOBILE ANDR")
@allure.tag("mobile", "auth")
@allure.feature("[ANDROID] Authentication")
class TestAuthMobile:

    @pytest.mark.smoke
    @allure.story("Successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://goodbudget.com/login", name="Login screen")
    @allure.description(
        "Checks successful authorization of a registered user in the mobile application."
    )
    def test_login_android_success(
        self, mobile_browser, credentials, login_screen, base_screen
    ):

        (
            login_screen.tap_login_entry()
            .type_name(credentials["username"])
            .type_password(credentials["password"])
            .submit()
        )
        base_screen.should_see_toast("Login Successful")

    @allure.story("Failed login with incorrect credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://goodbudget.com/login", name="Login screen")
    @allure.description(
        "Ensures that an error message is displayed when invalid data is entered."
    )
    def test_login_android_fail(self, mobile_browser, login_screen, base_screen):

        (
            login_screen.tap_login_entry()
            .type_name("fdgdhthtere")
            .type_password("643xretv2kHerr")
            .submit()
        )
        base_screen.should_see_toast("Login failed. Please try again.")

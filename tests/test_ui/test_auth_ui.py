import pytest, allure

@pytest.mark.ui
@pytest.mark.regression
@allure.tag("web", "auth")
@allure.feature("Authentication")
class TestAuthUi:

    @pytest.mark.smoke
    @allure.story("Login via UI")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://goodbudget.com/login", name="Login page")
    def test_login_ui(self,
            setup_browser,
            credentials,
            login_page,
            home_page
    ):

        (
            login_page
            .open()
            .fill_username(credentials["username"])
            .fill_password(credentials["password"])
            .submit_form()
        )
        home_page.user_greeting_should_be(credentials["username"])


    @allure.story("Logout via UI")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.link("https://goodbudget.com/home", name="Home")
    def test_logout_ui(self,
            setup_browser,
            credentials,
            home_page,
            logout_page,
            temp_cookie
    ):

        (
            home_page
            .open_home_with_cookie(credentials, temp_cookie)
            .logout_from_account()
        )

        logout_page.user_goodbye_should_be()

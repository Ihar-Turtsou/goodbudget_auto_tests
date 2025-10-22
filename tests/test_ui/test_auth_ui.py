import pytest, requests
from selene import have, browser


# @pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_login_ui(
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


# @pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_logout_ui(
        setup_browser,
        credentials,
        home_page, logout_page, temp_cookie
):

    (
        home_page
        .open_home_with_temp_cookie(credentials,temp_cookie)
        .logout_from_account()
    )

    logout_page.user_goodbye_should_be()

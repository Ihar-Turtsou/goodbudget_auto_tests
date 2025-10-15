import pytest
from selene import have, browser
import requests
from dotenv import load_dotenv
import os

@pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_login_ui(setup_browser, credentials):
    browser.open('/login')

    browser.element('[id="username"]').set_value(credentials["username"])
    browser.element('[id="password"]').set_value(credentials["password"])
    browser.element('form[action="/login_check"]').submit()

    browser.element('[id="hi"]').should(have.text(credentials["username"]))

@pytest.mark.skip(reason="This test is temporarily disabled.")
@pytest.mark.ui
def test_logout_ui(setup_browser, browser_logged_in):

    #
    # request = requests.post(
    #     url=BASE_URL + '/login_check',
    #     data={"_username":USERNAME,"_password":PASSWORD},
    #     allow_redirects=False
    # )

    # print(request.text)
    # print(request.cookies)
    # print(request.status_code)
    # cookie =request.cookies.get("GBSESS")
    # browser.open(f'{BASE_URL}/home')
    # browser.driver.add_cookie({"name": "GBSESS", "value":cookie})
    # browser.open(f'{BASE_URL}/home')



    browser.element('a[href="/logout"]').click()
    browser.element('h3.elementor-heading-title').should(
        have.exact_text("You've been successfully logged out")
    )

# python -m pytest -s
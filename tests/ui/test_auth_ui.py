import pytest
from selene import have, browser
import requests
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv('GB_BASE_URL')
USERNAME = os.getenv('GB_USERNAME')
PASSWORD = os.getenv('GB_PASSWORD')

@pytest.mark.ui
def test_login_ui(setup_browser):
    browser.open('/login')

    browser.element('[id="username"]').set_value(USERNAME)
    browser.element('[id="password"]').set_value(PASSWORD)
    browser.element('form[action="/login_check"]').submit()

    browser.element('[id="hi"]').should(have.text(USERNAME))

@pytest.mark.ui
def test_logout_ui(setup_browser):
    request = requests.post(
        url=BASE_URL + '/login_check',
        data={"_username":USERNAME,"_password":PASSWORD},
        allow_redirects=False
    )

    # print(request.text)
    # print(request.cookies)
    # print(request.status_code)
    cookie =request.cookies.get("GBSESS")
    browser.open(f'{BASE_URL}/home')
    browser.driver.add_cookie({"name": "GBSESS", "value":cookie})
    browser.open(f'{BASE_URL}/home')
    browser.element('a[href="/logout"]').click()
    browser.element('h3.elementor-heading-title').should(
        have.exact_text("You've been successfully logged out")
    )

# python -m pytest -s
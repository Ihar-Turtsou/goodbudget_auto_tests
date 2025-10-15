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

    browser.element('a[href="/logout"]').click()
    browser.element('h3.elementor-heading-title').should(
        have.exact_text("You've been successfully logged out")
    )

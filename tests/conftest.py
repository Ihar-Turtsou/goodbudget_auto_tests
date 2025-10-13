import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from dotenv import load_dotenv
import os
from selene import browser
from utils import attach
import requests


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def credentials():
    return {
        "base_url": os.getenv("GB_BASE_URL", "https://goodbudget.com"),
        "username": os.getenv("GB_USERNAME"),
        "password": os.getenv("GB_PASSWORD"),
    }



@pytest.fixture(scope="session")
def session_cookie():
    base_url = os.getenv("GB_BASE_URL", "https://goodbudget.com")
    username = os.getenv("GB_USERNAME")
    password = os.getenv("GB_PASSWORD")

    session = requests.Session()
    session.get(f"{base_url}/login", timeout=15)
    response = session.post(
        f"{base_url}/login_check",
        data={"_username": username, "_password": password},
        allow_redirects=False,
        timeout=15,
    )
    assert response.status_code in (302, 303), f"Login failed: {response.status_code}"
    cookie_value = session.cookies.get("GBSESS")
    assert cookie_value, "GBSESS cookie not set"
    return cookie_value


@pytest.fixture
def browser_logged_in(session_cookie):
    browser.open("/")
    browser.driver.add_cookie({
        "name": "GBSESS",
        "value": session_cookie,
        "path": "/",
        "domain": "goodbudget.com",
    })
    browser.open("/home")
    yield

# @pytest.fixture(scope="function")
# def remote_browser_setup(request):
#
#     selenoid_login = os.getenv("SELENOID_LOGIN")
#     selenoid_pass = os.getenv("SELENOID_PASS")
#     selenoid_url = os.getenv("SELENOID_URL")
#
#     options = Options()
#     options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
#     selenoid_capabilities = {
#         "browserName": "chrome",
#         "browserVersion": "128.0",
#         "selenoid:options": {
#             "enableVNC": True,
#             "enableVideo": True
#         }
#     }
#
#     options.capabilities.update(selenoid_capabilities)
#     driver = webdriver.Remote(
#         command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
#         options=options)
#
#     browser.config.driver = driver
#     yield browser
#     attach.add_logs(browser)
#     attach.add_html(browser)
#     attach.add_screenshot(browser)
#     attach.add_video(browser)
#
#     try:
#         browser.quit()
#     except (InvalidSessionIdException, WebDriverException):
#         pass

@pytest.fixture(autouse=True)
def setup_browser():
    browser.config.base_url = 'https://goodbudget.com'
    browser.config.timeout = 5
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    yield
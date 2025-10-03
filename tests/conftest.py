import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from dotenv import load_dotenv
import os
from selene import browser
from utils import attach


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope="function")
def remote_browser_setup(request):

    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    options = Options()
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }

    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options)

    browser.config.driver = driver
    yield browser
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_video(browser)

    try:
        browser.quit()
    except (InvalidSessionIdException, WebDriverException):
        pass

@pytest.fixture(autouse=True)
def setup_browser(remote_browser_setup):
    browser.config.base_url = 'https://www.url.url/'
    browser.config.timeout = 5
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    yield
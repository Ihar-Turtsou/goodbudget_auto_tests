import pytest, allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from dotenv import load_dotenv
import os
from selene import browser
from utils import attach
from appium import webdriver
import requests
from goodbudget.ui.pages.login_page import LoginPage
from goodbudget.ui.pages.home_page import HomePage
from goodbudget.ui.pages.logout_page import LogoutPage
from goodbudget.mobile.screens.base_screen import BaseScreen
from goodbudget.mobile.screens.login_screen import LoginScreen
from goodbudget.mobile.screens.home_screen import HomeScreen
from goodbudget.mobile.screens.onboarding_screen import OnboardingScreen
from appium import webdriver
from appium.options.android import UiAutomator2Options
import pytest
import sys
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import get_local_config, get_bs_config



def pytest_addoption(parser):
    parser.addoption(
        "--local",
        action="store_true",
        default=False,
        help="Run mobile tests locally instead of BrowserStack",
    )



@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def credentials():
    return {
        "base_url": os.getenv("GB_BASE_URL", "https://goodbudget.com"),
        "username": os.getenv("GB_USERNAME"),
        "password": os.getenv("GB_PASSWORD"),
        "household_id":os.getenv("HOUSEHOLD_ID"),
        "account_uuid": os.getenv("ACCOUNT_UUID")
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
def temp_cookie(credentials):
    session = requests.Session()
    session.get(f'{credentials["base_url"]}/login', timeout=15)
    request = session.post(
        f'{credentials["base_url"]}/login_check',
        data={"_username": credentials["username"], "_password": credentials["password"]},
        allow_redirects=False, timeout=15
    )
    cookie = session.cookies.get("GBSESS")
    assert cookie
    return cookie


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


@pytest.fixture()
def login_page():
    return LoginPage()

@pytest.fixture()
def logout_page():
    return LogoutPage()

@pytest.fixture()
def home_page():
    return HomePage()

@pytest.fixture()
def login_screen():
    return LoginScreen()

@pytest.fixture()
def base_screen():
    return BaseScreen()

@pytest.fixture()
def home_screen():
    return HomeScreen()

@pytest.fixture()
def onboarding_screen():
    return OnboardingScreen()


@pytest.fixture(autouse=True)
def setup_browser():

    browser.config.base_url = 'https://goodbudget.com'
    browser.config.timeout = 5
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    yield



@pytest.fixture(scope="function")
def mobile_driver(request):

    is_local = request.config.getoption("--local")

    if is_local:
        cfg = get_local_config()

        caps = {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:deviceName": cfg.device_name,
            "appium:app": cfg.app_path,
            "appium:appWaitActivity": "*",
            "appium:appWaitForLaunch": False,
            "appium:autoGrantPermissions": True,
            "appium:fullReset": False,
            "appium:noReset": False,
        }
        options = UiAutomator2Options().load_capabilities(caps)
        driver = webdriver.Remote(cfg.appium_url, options=options)
        yield driver
        driver.quit()

    else:
        bs = get_bs_config()
        caps = {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:deviceName": bs.device_name,
            "appium:platformVersion": bs.platform_version,
            "appium:app": bs.app_id,
            "appium:fullReset": False,
            "appium:noReset": False,
            "bstack:options": {
                "projectName": "Goodbudget AutoTests",
                "buildName": "Mobile BS Run",
                "sessionName": "Smoke test",
            },
        }
        options = UiAutomator2Options().load_capabilities(caps)
        driver = webdriver.Remote(
            f"https://{bs.user}:{bs.key}@hub.browserstack.com/wd/hub",
            options=options,
        )
        yield driver
        try:
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", '
                '"arguments": {"status":"passed","reason":"pytest finished"}}'
            )
        except Exception:
            pass
        driver.quit()


@pytest.fixture(scope="session", autouse=True)
def reset_before_run():
    package = "com.dayspringtech.envelopes"
    check = os.popen(f"adb shell pm list packages | grep {package}").read()
    if package in check:
        os.system(f"adb uninstall {package}")
    else:
        print(f"The {package} application is not installed.")

@pytest.fixture(scope="session", autouse=True)
def uninstall_app_after_all_tests():
    yield
    try:
        os.system("adb uninstall com.dayspringtech.envelopes")
    except Exception as e:
        print(f"Failed to uninstall app: {e}")
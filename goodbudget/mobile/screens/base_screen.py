import allure
from selene import browser
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseScreen:
    @property
    def driver(self):
        return browser.config.driver

    @allure.step('Expect toast with text: {text}')
    def should_see_toast(self, text, timeout: int = 10):
        toast = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, f"//android.widget.Toast[@text='{text}']")
            )
        )
        return toast
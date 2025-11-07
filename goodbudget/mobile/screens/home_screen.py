import allure
from selene import be, browser


class HomeScreen:

    @allure.step("User visible: {name} on Home")
    def should_see_username(self, name):
        browser.element(f'//android.widget.TextView[@text="{name}"]').should(be.visible)
        return self

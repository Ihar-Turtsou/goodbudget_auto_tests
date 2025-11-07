import allure
from selene import browser, have


class LogoutPage:

    @allure.step("Verify successful logout message is displayed")
    def user_goodbye_should_be(self):
        browser.element("h3.elementor-heading-title").should(
            have.exact_text("You've been successfully logged out")
        )
        return self

from selene import have, browser

class LogoutPage:

    def user_goodbye_should_be(self):
        browser.element('h3.elementor-heading-title').should(
            have.exact_text("You've been successfully logged out")
        )
        return self
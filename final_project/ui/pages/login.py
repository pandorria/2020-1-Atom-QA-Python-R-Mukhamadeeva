from ui.locators import LoginLocators
from ui.pages.base_page import BasePage


class LoginPage(BasePage):
    locators = LoginLocators()

    def login(self, username, password):
        self.input(username, self.locators.USERNAME_INPUT)
        self.input(password, self.locators.PASSWORD_INPUT)
        self.click(self.locators.LOGIN_BUTTON)

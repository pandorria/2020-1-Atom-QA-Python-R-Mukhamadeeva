from ui.locators.locators import LoginLocators
from ui.pages.base import BasePage


class LoginPage(BasePage):
    locators = LoginLocators()

    def login(self, username, password):
        self.click(self.locators.COMEIN_BUTTON)
        self.input(username, self.locators.EMAIL_INPUT)
        self.input(password, self.locators.PASSWORD_INPUT)
        self.click(self.locators.LOGIN_BUTTON)

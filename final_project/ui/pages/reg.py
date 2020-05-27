from ui.locators import RegLocators
from ui.pages.base_page import BasePage


class RegPage(BasePage):
    locators = RegLocators()

    def reg(self, username, email, password, repeat_password=None):
        self.click(self.locators.CREATE_ACCOUNT)
        self.input(username, self.locators.USERNAME_INPUT)
        self.input(email, self.locators.EMAIL_INPUT)
        self.input(password, self.locators.PASSWORD_INPUT)
        self.input(repeat_password or password, self.locators.PASSWORD_REPEAT_INPUT)
        self.click(self.locators.ACCEPT_CHECKBOX)
        self.click(self.locators.REG_BUTTON)

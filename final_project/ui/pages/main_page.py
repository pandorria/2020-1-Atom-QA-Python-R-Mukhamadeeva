from ui.locators import LoginLocators, MainPageLocators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    locators = MainPageLocators()

    def logout(self):
        self.click(self.locators.LOGOUT)



from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from ui.locators.locators import LoginLocators


class BasePage:
    locators = LoginLocators()

    def __init__(self, driver):
        self.driver = driver

    def input(self, query, locator):
        input_field = self.find(locator)
        input_field.clear()
        input_field.send_keys(query)

    def find(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def click(self, locator, timeout=None):
        if isinstance(locator[1], list):
            locators = locator[1]
        else:
            locators = [locator[1]]
        for i in locators:
            current_locator = (locator[0], i)
            try:
                self.find(current_locator)
                element = self.wait(timeout).until(EC.element_to_be_clickable(current_locator))
                element.click()
                return
            except Exception as e:
                print(e)
                continue
        raise

    def scroll_to_element(self, element):
        self.driver.execute_script('arguments[0].scrollIntoView(true);', element)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def is_invisibility(self, locator):
        element = self.find(locator)
        return self.wait().until(EC.invisibility_of_element_located(element))

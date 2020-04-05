from ui.locators.locators import CreateSegment
from ui.pages.login import LoginPage


class CreateSegment(LoginPage):
    locators = CreateSegment

    def create_segment(self, segment_name):
        self.login('test.qa20@yandex.ru', 'QWer1@')
        self.click(self.locators.AUDITORY_BUTTON)
        self.click(self.locators.CREATE_SEGMENT)
        self.click(self.locators.INPUT_NAME)
        self.input(segment_name, self.locators.INPUT_NAME)
        self.click(self.locators.ADD_SEGMENT)
        self.click(self.locators.CHECKBOX)
        self.click(self.locators.ADD_SEGMENT_FINAL)
        self.click(self.locators.DONE)
        self.find(self.locators.CHECK_IS_CREATED)

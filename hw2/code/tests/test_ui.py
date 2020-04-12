import pytest
from tests.base import BaseCase
import os


class Test(BaseCase):
    @pytest.mark.UI
    def test_login(self):
        self.login_page.login('test.qa20@yandex.ru', 'QWer1@')
        assert "Invalid login or password" not in self.driver.page_source

    @pytest.mark.UI
    def test_login_negative(self):
        self.login_page.login('test.qa20@yandex.ru', 'vcf3dmkl')
        assert "Invalid login or password" in self.driver.page_source

    @pytest.mark.UI
    def test_create_advert(self):
        self.advert.login('test.qa20@yandex.ru', 'QWer1@')
        self.advert.click(self.advert.locators.COMPANY_BUTTON)
        self.advert.click(self.advert.locators.NEW_CAMPAIGN, timeout=20)
        self.advert.click(self.advert.locators.AUDIO_ADVERT, timeout=20)
        self.advert.find(self.advert.locators.ADD_AUDIO).send_keys(os.path.dirname(__file__) + "/audio.mp3")
        self.advert.click(self.advert.locators.ADD_ADVERT, timeout=20)
        self.advert.find(self.advert.locators.DONE, timeout=10)
        assert "Создана рекламная кампания" in self.driver.page_source

    @pytest.mark.UI
    def test_create_segment(self):
        segment_name = "test_create_segment"
        self.segment.create_segment(segment_name)
        assert segment_name in self.driver.page_source

    @pytest.mark.UI
    def test_delete_segment(self):
        segment_name = "test_delete_segment"
        self.segment.create_segment(segment_name)
        self.segment_delete.click(self.segment_delete.locators.detele_selected_segment(segment_name))
        self.segment_delete.click(self.segment_delete.locators.DELETE_SEGMENT)
        self.segment_delete.is_invisibility(self.segment_delete.locators.CHECK_IS_CREATED)
        assert segment_name not in self.driver.page_source


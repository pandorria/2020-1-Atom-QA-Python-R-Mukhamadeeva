import pytest

from ui.pages.advert import CreateAdvert
from ui.pages.login import LoginPage
from ui.pages.segment import CreateSegment
from ui.pages.segment_delete import SegmentDelete


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver = driver
        self.config = config
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.advert: CreateAdvert = request.getfixturevalue('advert')
        self.segment: CreateSegment = request.getfixturevalue('segment')
        self.segment_delete: SegmentDelete = request.getfixturevalue('segment_delete')

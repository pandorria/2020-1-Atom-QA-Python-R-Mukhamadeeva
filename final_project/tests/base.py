import pytest
import strgen

from ui.pages.login import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.reg import RegPage


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request):
        self.driver = driver
        self.config = config
        self.reg_page: RegPage = request.getfixturevalue('reg_page')
        self.login_page: LoginPage = request.getfixturevalue('login_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')


def generate_user(len_user=6, len_pass=6, russian_username=False, russian_email=False, mask=True):
    username = strgen.StringGenerator('[a-z]{%d}' % len_user if not russian_username else '[а-я]{%d}' % len_user).render()
    if mask:
        email = strgen.StringGenerator('[a-z]{3:5}@[\c]{3:4}.(com|net|ru)').render()
    elif russian_email:
        email = strgen.StringGenerator('[а-я]{3:5}@[\c]{3:4}.(com|net|ru)').render()
    else:
        email = strgen.StringGenerator('[a-z]{10}').render()
    password = strgen.StringGenerator('[a-zZ-A0-9]{%d}' % len_pass).render()
    return username, email, password

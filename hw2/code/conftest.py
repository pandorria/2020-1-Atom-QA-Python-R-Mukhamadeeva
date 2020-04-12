from ui.fixtures import *
import pytest
from api.mytarget_client import MyTargetClient


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com/')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--browser_ver', default='80.0')
    parser.addoption('--selenoid', default=None)


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    selenoid = request.config.getoption('--selenoid')
    return {'browser': browser, 'version': version, 'url': url, 'selenoid': selenoid}


@pytest.fixture(scope='function')
def api_client(email, password):
    return MyTargetClient(email, password)

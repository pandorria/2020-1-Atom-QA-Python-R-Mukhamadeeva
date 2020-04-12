import pytest

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from ui.pages.advert import CreateAdvert
from ui.pages.segment_delete import SegmentDelete
from ui.pages.segment import CreateSegment
from ui.pages.login import LoginPage


class UnsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope='function')
def advert(driver):
    return CreateAdvert(driver)


@pytest.fixture(scope='function')
def segment(driver):
    return CreateSegment(driver)


@pytest.fixture(scope='function')
def segment_delete(driver):
    return SegmentDelete(driver)


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    url = config['url']
    selenoid = config['selenoid']
    if selenoid:
        host, port = selenoid.split(':')
        options = ChromeOptions()
        options.add_argument("--window-size=800,600")

        capabilities = {'acceptInsecureCerts': True,
                        'browserName': 'chrome',
                        'version': version,
                        }

        driver = webdriver.Remote(command_executor=f'http://{host}:{port}/wd/hub/',
                                  options=options,
                                  desired_capabilities=capabilities
                                  )
    elif browser == 'chrome':
        options = ChromeOptions()
        options.add_argument("--window-size=2560, 1600")

        capabilities = {'acceptInsecureCerts': True,
                        'browserName': 'chrome',
                        'version': version,
                        }

        driver = webdriver.Chrome(
            options=options,
            desired_capabilities=capabilities
        )
    else:
        raise UnsupportedBrowserException(f'Usupported browser: "{browser}"')

    driver.get(url)
    driver.fullscreen_window()
    yield driver
    driver.close()

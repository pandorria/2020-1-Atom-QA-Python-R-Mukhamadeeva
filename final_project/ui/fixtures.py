import pytest

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from ui.pages.login import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.reg import RegPage


class UnsupportedBrowserException(Exception):
    pass


@pytest.fixture(scope='function')
def reg_page(driver):
    return RegPage(driver)


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture(scope='function')
def main_page(driver):
    return MainPage(driver)


@pytest.fixture(scope='function')
def driver(config):
    browser = config['browser']
    version = config['version']
    selenoid = config['selenoid']
    if selenoid:
        url = f'http://{config["app_name"]}:{config["port"]}'
        host, port = selenoid.split(':')

        capabilities = {
            "browserName": "chrome",
            "version": "83.0",
            "enableVNC": False,
            "enableVideo": False,
            "applicationContainers": [config["app_name"]],
        }

        driver = webdriver.Remote(command_executor=f'http://{host}:{port}/wd/hub/',
                                  desired_capabilities=capabilities
                                  )
    elif browser == 'chrome':
        url = f'http://{config["host"]}:{config["port"]}'
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

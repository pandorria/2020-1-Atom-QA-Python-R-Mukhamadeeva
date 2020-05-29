import os
import time

import allure
import docker

from api.api_client import ApiClient
from orm.orm_client import MysqlOrmConnection
from orm.orm_builder import MysqlOrmBuilder
from ui.fixtures import *

app_name = 'test_server'


def pytest_addoption(parser):
    global app_name
    parser.addoption('--host', default='0.0.0.0')
    parser.addoption('--post', default='3000')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--browser_ver', default='83..0')
    parser.addoption('--selenoid', default='127.0.0.1:4444')
    parser.addoption('--app_name', default=app_name)


@pytest.fixture(scope='session')
def config(request):
    host = request.config.getoption('--host')
    port = request.config.getoption('--post')
    application_name = request.config.getoption('--app_name')
    browser = request.config.getoption('--browser')
    version = request.config.getoption('--browser_ver')
    selenoid = request.config.getoption('--selenoid')
    return {'browser': browser, 'version': version, 'host': host,
            'port': port, 'selenoid': selenoid, 'app_name': application_name}


@pytest.fixture(scope='function')
def api_client(username, password, email):
    return ApiClient(username, password, email)


@pytest.fixture(scope='session')
def mysql_orm_client():
    return MysqlOrmConnection('root', 'renata', 'users')


@pytest.fixture(scope="session", autouse=True)
def start_session(request):
    global app_name
    containers = []
    mock_port = 5000
    mysql_name = 'mysql_db'
    mysql_port = 3306
    app_port = 3000
    client = docker.from_env()
    try:
        mysql_container = client.containers.run('mysql:latest', detach=True, ports={f'{mysql_port}/tcp': mysql_port},
                                                name=mysql_name,
                                                environment={'MYSQL_ROOT_PASSWORD': 'renata'},
                                                )
    except:
        time.sleep(60)
        return None
    containers.append(mysql_container)
    time.sleep(40)
    MysqlOrmBuilder(MysqlOrmConnection('root', 'renata', 'users'))

    mock_container = client.containers.run('vk_api:latest', detach=True, ports={f'{mock_port}/tcp': mock_port})
    mock_name = mock_container.name
    containers.append(mock_container)

    with open('config/config.docker', 'w') as f:
        f.write("APP_HOST = '0.0.0.0'\n")
        f.write(f"APP_PORT = {app_port}\n")
        f.write(f"MYSQL_HOST = {mysql_name}\n")
        f.write(f"MYSQL_PORT = {mysql_port}\n")
        f.write("MYSQL_DB = users\n")
        f.write(f"VK_URL = localhost:{mock_port}\n")
    app_container = client.containers.run('myapp',
                                          command=' /app/myapp --config="/home/config.docker"',
                                          name=app_name,
                                          detach=True, ports={f'{app_port}/tcp': app_port},
                                          links={mysql_name: '127.0.0.1', mock_name: 'localhost'},
                                          volumes={
                                              os.path.join(os.getcwd(), 'config'): {'bind': '/home/', 'mode': 'rw'}})
    containers.append(app_container)
    time.sleep(10)

    def stop_session():
        for i in containers:
            i.stop()
            i.remove()

    request.addfinalizer(stop_session)


@pytest.fixture(scope="function")
def take_screenshot_when_failure(request, driver):
    yield
    if request.node.rep_call.failed:
        allure.attach('\n'.join(driver.get_log('browser')),
                      name='console.log',
                      attachment_type=allure.attachment_type.TEXT)
        allure.attach(driver.get_screenshot_as_png(),
                      name=request.node.location[-1],
                      attachment_type=allure.attachment_type.PNG)

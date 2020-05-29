import pytest
import allure
from tests.base import BaseCase, generate_user
from orm.orm_client import MysqlOrmConnection
from orm.orm_builder import MysqlOrmBuilder
import time


class TestReg(BaseCase):

    @pytest.fixture(scope='function', autouse=True)
    def database(self, mysql_orm_client):
        self.mysql: MysqlOrmConnection = mysql_orm_client
        self.builder = MysqlOrmBuilder(mysql_orm_client)

    def test_reg_success(self):
        """
        Тестируется сценарий регистрации нового пользователя. Все поля введены корректно, регистрация проходит успешно
        и пользователю открывается главная страница приложения. В базе выставляется флаг access равный 1
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        result_flag = self.builder.get_access(username)
        self.builder.del_user(username)
        assert "powered by ТЕХНОАТОМ" in self.driver.page_source
        assert result_flag == 1

    def test_reg_exist_user(self):
        """
        Тестируется негативный сценарий, когда производится попытка зарегестрировать уже существующего в базе
        пользователя.
        Приложение работает корректно и пользователю выводится сообщение об ошибке
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.logout()
        self.reg_page.reg(username, email, password)
        assert "User already exist" in self.driver.page_source
        self.builder.del_user(username)

    def test_reg_incorrect_username_length_min(self):
        """
        Тестируется негативный сценарий, когда производится попытка зарегестрировать пользователя с длиной поля
        usеrname, не проходящей минимальную допустимую границу
        Приложение работает корректно и пользователю выводится сообщение об ошибке
        """
        username, email, password = generate_user(len_user=5)
        self.reg_page.reg(username, email, password)
        assert "Incorrect username length" in self.driver.page_source
        self.builder.del_user(username)

    def test_reg_incorrect_username_length_max(self):
        """
        Тестируется негативный сценарий, когда производится попытка зарегестрировать пользователя с длиной поля
        usеrname, превышающей максимальную допустимую границу
        Приложение работает корректно и пользователю выводится сообщение об ошибке
        """
        username, email, password = generate_user(len_user=17)
        self.reg_page.reg(username, email, password)
        assert "Incorrect username length" in self.driver.page_source
        self.builder.del_user(username)

    def test_reg_incorrect_password_length(self):
        """
        Тестируется возможность пройти регистрацию с длиной значений password = 1
        Приложение должно выдавать ошибку в силу соображений тестирования безопасности
        Приложение работает некорректно и регистрация проходит успешно
        """
        username, email, password = generate_user(len_pass=1)
        self.reg_page.reg(username, email, password)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name='test_python_link',
                      attachment_type=allure.attachment_type.PNG)
        assert "Incorrect password length" in self.driver.page_source
        self.builder.del_user(username)

    def test_reg_russian_username(self):
        """
        Тестируется возможность пройти регистрацию с русским значением поля username.
        Приложение должно выдавать ошибку в силу следующих причин:
        1. В любом сервисе данное поле заполняется на универсальном английском языке и почти всегда должно
        быть уникально(это в данном случае предусмотрено)
        2. Приложение подразумевает использование VK API, для работы которого необходимо передавать username на англ.
        """
        username, email, password = generate_user(russian_username=True)
        self.reg_page.reg(username, email, password)
        self.builder.del_user(username)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name='test_python_link',
                      attachment_type=allure.attachment_type.PNG)
        assert "Incorrect username" in self.driver.page_source

    def test_reg_repeat_password_negative(self):
        """
        Тестируется негативный сценарий, когда пароли не совпадают при регистрации
        Приложение работает корректно
        Пользователю выводится сообщение об ошибке
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password, generate_user()[2])
        assert "Passwords must match" in self.driver.page_source
        self.builder.del_user(username)

    def test_reg_russian_email(self):
        """
        Тестируется возможность пройти регистрацию с русским значением поля email. Приложение должно выдавать ошибку,
        т.к. email ни при каких условиях не может принимать русские значения
        """
        username, email, password = generate_user(russian_email=True)
        self.reg_page.reg(username, email, password)
        self.builder.del_user(username)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name='test_python_link',
                      attachment_type=allure.attachment_type.PNG)
        assert "Invalid email address" in self.driver.page_source

    def test_reg_invalid_email(self):
        """
        Тестируется возможность пройти регистрацию со значением email, не проходящим под стандартную маску ввода
        Приложение ведет себя корректно и пользователю выводится сообщение об ошибке
        """
        username, email, password = generate_user(mask=False)
        self.reg_page.reg(username, email, password)
        assert "Invalid email address" in self.driver.page_source
        self.builder.del_user(username)

    def test_reg_exist_email(self):
        """
        Тестируется возможность регистрации пользователя с уже существуещем email.
        Приложение ведет себя некорректно, возникает 500-ая ошибка
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.logout()
        self.reg_page.reg(generate_user()[0], email, password)
        self.builder.del_user(username)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name='test_python_link',
                      attachment_type=allure.attachment_type.PNG)
        assert "Email already exist" in self.driver.page_source

    def test_reg_several_incorrect_fields(self):
        """
        Тестируется сценарий, когда пользователь при регистрации допустил ошибки в более чем 1-м поле ввода.
        Приложение выводит ошибку в виде словаря из некорректных данных, не прилагая пояснительный текст с описанием
        возникших проблем для обычного пользователя
        """
        username, email, password = generate_user(len_user=1, mask=False)
        self.reg_page.reg(username, email, password, generate_user()[2])
        allure.attach(self.driver.get_screenshot_as_png(),
                      name='test_python_link',
                      attachment_type=allure.attachment_type.PNG)
        assert "Incorrect username length, incorrect email address, passwords must match" in self.driver.page_source


class TestLogin(BaseCase):
    @pytest.fixture(scope='function', autouse=True)
    def database(self, mysql_orm_client):
        self.mysql: MysqlOrmConnection = mysql_orm_client
        self.builder = MysqlOrmBuilder(mysql_orm_client)

    def test_login(self):
        """
        Тестируется сценарий авторизации зарегестрированного в приложении пользователя. Приложение работает корректно,
        после авторизации пользвателю доступна главная страница
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.logout()
        self.login_page.login(username, password)
        self.builder.del_user(username)
        assert "powered by ТЕХНОАТОМ" in self.driver.page_source

    def test_login_negative(self):
        """
        Тестируется негативный сценарий авторизации с неверно введенным логином или паролем.
        Приложение работает корректно, пользователю выводится сообщение об ошибке
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.logout()
        self.login_page.login(generate_user()[0], password)
        self.builder.del_user(username)
        assert "Invalid username or password" in self.driver.page_source

    def test_button_create_account(self):
        """
        Тестируется переход со страницы авторизации на страницу регистрации.
        Приложение работает корректно, после нажатия на кнопку Create an account пользователь переходит
        на страницу регистрации
        """
        self.login_page.click(self.login_page.locators.CREATE_ACCOUNT)
        assert "Registration" in self.driver.page_source

    def test_button_log_in(self):
        """
        Тестируется переход со страницы регистрации на страницу авторизации.
        Приложение работает корректно, после нажатия на кнопку Log in пользователь переходиит на страницу авторизации
        """
        self.login_page.click(self.login_page.locators.CREATE_ACCOUNT)
        self.reg_page.click(self.reg_page.locators.LOG_IN)
        assert "Welcome to the TEST SERVER" in self.driver.page_source


class TestMainPage(BaseCase):
    @pytest.fixture(scope='function', autouse=True)
    def database(self, mysql_orm_client):
        self.mysql: MysqlOrmConnection = mysql_orm_client
        self.builder = MysqlOrmBuilder(mysql_orm_client)

    def test_logout(self):
        """
        Тестируется кнопка выхода  Logout, расположенная на главной странице приложения
        Приложение работает корректно, после нажатия на данную кнопку пользователь переходит на страницу авторизации
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.logout()
        self.builder.del_user(username)
        assert "Welcome to the TEST SERVER" in self.driver.page_source

    def test_logout_access_flag(self):
        """
        Тестируется изменение флага access с 1 на 0 при нажатии кнопки Logout, расположенной на главной странице
        Приложение работает некорректно, после выхода из аккаунта флаг сохраняет значение 1
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.logout()
        result_flag = self.builder.get_access(username)
        self.builder.del_user(username)
        assert result_flag == 0

    def test_logged_as(self):
        """
        Тестируется появление имени пользователя на главной страние при успешной авторизации в приложении
        Приложение работает корректно, на главной странице отображается logged as {username}
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.builder.del_user(username)
        assert f'logged as {username}' in self.driver.page_source

    def test_api_link(self):
        """
        Тестируется клик и переход на внешний ресурс "What is an API?"
        Проверяется не только переход на страницу запрашиваемого ресурса, но и его открытие в новой вкладке браузера
        Приложение работает корректно, в новой вкладке открывается запрашиваемый ресурс
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.click(self.main_page.locators.API_LOCATOR)
        self.builder.del_user(username)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://en.wikipedia.org/wiki/Application_programming_interface" == self.driver.current_url

    def test_internet_future_link(self):
        """
        Тестируется клик и переход на внешний ресурс "Future of internet"
        Проверяется не только переход на страницу запрашиваемого ресурса, но и его открытие в новой вкладке браузера
        Приложение работает корректно, в новой вкладке открывается запрашиваемый ресурс
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.click(self.main_page.locators.INTERNET_LOCATOR)
        self.builder.del_user(username)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/" \
               == self.driver.current_url

    def test_smtp_link(self):
        """
        Тестируется клик и переход на внешний ресурс "Lets talk about SMTP?"
        Проверяется не только переход на страницу запрашиваемого ресурса, но и его открытие в новой вкладке браузера
        Приложение работает корректно, в новой вкладке открывается запрашиваемый ресурс
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.click(self.main_page.locators.SMTP_LOCATOR)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.builder.del_user(username)
        assert "https://ru.wikipedia.org/wiki/SMTP" == self.driver.current_url

    def test_change_phrase(self):
        """
        Тестируется обновление цитаты в нижней части страницы при обновлении главной страницы приложения
        Приложение работает корректно, при обновлении страницы генерируется новая цитата
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        phrase = self.main_page.find(self.main_page.locators.PHRASE_LOCATOR).text
        self.driver.refresh()
        self.builder.del_user(username)
        assert phrase != self.main_page.find(self.main_page.locators.PHRASE_LOCATOR).text

    def test_python_link(self):
        """
        Тестируется ссылка с переходом на сайт python.org
        Ссылка является внешним ресурсом и страницы должна открываться в новой вкладке браузера.
        Приложение работает некорректно и остается на текущей странице
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.click(self.main_page.locators.PYTHON_LOCATOR)
        self.builder.del_user(username)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name='test_python_link',
                      attachment_type=allure.attachment_type.PNG)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://www.python.org/" == self.driver.current_url

    def test_python_history(self):
        """
        Тестируется элемент Python history из выпадающего списка, появляющегося после наведения на элемент Python
        из горизонтального меню.
        После нажатия на элемент приложение отрабатывает некорректно, т.к запрашиваемый внешний ресурс отерывается
        в текущем окне браузера
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.move(self.main_page.locators.PYTHON_LOCATOR)
        self.main_page.click(self.main_page.locators.PYTHON_HISTORY)
        self.builder.del_user(username)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://en.wikipedia.org/wiki/History_of_Python" == self.driver.current_url

    def test_about_flask(self):
        """
        Тестируется элемент About flask из выпадающего списка, появляющегося после наведения на элемент Python
        из горизонтального меню.
        После нажатия на элемент приложение отрабатывает корректно и в новом окне браузера открывает
        запрашиваемый ресурс
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.move(self.main_page.locators.PYTHON_LOCATOR)
        self.main_page.click(self.main_page.locators.FLASK_LOCATOR)
        self.builder.del_user(username)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://flask.palletsprojects.com/en/1.1.x/#" == self.driver.current_url

    def test_linux_link(self):
        """
        Тестируется ссылка с переходом на сайт linux из горизонтального меню.
        Данный элемент стоит в ряду, который подразумевает, что каждый в нем находящийся элемент является линком.
        Тест падает, потому что ссылка является неактивной
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.click(self.main_page.locators.LINUX_LOCATOR)
        self.builder.del_user(username)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name='test_python_link',
                      attachment_type=allure.attachment_type.PNG)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://www.linuxfoundation.org/" == self.driver.current_url

    def test_centos(self):
        """
        Тестируется элемент Download Centos7 из выпадающего списка, появляющегося после наведения на элемент Linux
        из горизонтального меню.
        После нажатия на элемент, приложение проходит перввую проверку и открывает ссылку в новой вкладке, вторую
        проверку тест не прошел, т.к. url не совпадает с ожидаемым.
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.move(self.main_page.locators.LINUX_LOCATOR)
        self.main_page.click(self.main_page.locators.CENTOS_LOCATOR)
        self.builder.del_user(username)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        allure.attach(self.driver.get_screenshot_as_png(),
                      name='test_python_link',
                      attachment_type=allure.attachment_type.PNG)
        assert "https://www.centos.org/download/" == self.driver.current_url

    def test_network_link(self):
        """
        Тестируется ссылка с переходом на ресурс Network из горизонтального меню.
        Данный элемент стоит в ряду, который подразумевает, что каждый в нем находящийся элемент является линком.
        Тест падает, потому что ссылка является неактивной

        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.click(self.main_page.locators.NETWORK_LOCATOR)
        self.builder.del_user(username)
        allure.attach(self.driver.get_screenshot_as_png(),
                      name='test_python_link',
                      attachment_type=allure.attachment_type.PNG)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://en.wikipedia.org/wiki/Network" == self.driver.current_url

    def test_wireshark_news(self):
        """
        Тестируется элемент News из выпадающего списка, появляющегося после наведения на элемент Linux
        из горизонтального меню.
        После нажатия на элемент приложение отрабатывает корректно и в новом окне браузера открывает
        запрашиваемый ресурс
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.move(self.main_page.locators.NETWORK_LOCATOR)
        self.main_page.click(self.main_page.locators.NEWS_LOCATOR)
        self.builder.del_user(username)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://www.wireshark.org/news/" == self.driver.current_url

    def test_wireshark_download(self):
        """
        Тестируется элемент Download из выпадающего списка, появляющегося после наведения на элемент Linux
        из горизонтального меню.
        После нажатия на элемент приложение отрабатывает корректно и в новом окне браузера открывает
        запрашиваемый ресурс
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.move(self.main_page.locators.NETWORK_LOCATOR)
        self.main_page.click(self.main_page.locators.DOWNLOAD_LOCATOR)
        self.builder.del_user(username)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://www.wireshark.org/#download" == self.driver.current_url

    def test_examples(self):
        """
        Тестируется элемент Examples из выпадающего списка, появляющегося после наведения на элемент Linux
        из горизонтального меню.
        После нажатия на элемент приложение отрабатывает корректно и в новом окне браузера открывает
        запрашиваемый ресурс
        """
        username, email, password = generate_user()
        self.reg_page.reg(username, email, password)
        self.main_page.move(self.main_page.locators.NETWORK_LOCATOR)
        self.main_page.click(self.main_page.locators.EXAMPLES_LOCATOR)
        self.builder.del_user(username)
        assert len(self.driver.window_handles) == 2
        self.driver.switch_to.window(self.driver.window_handles[-1])
        assert "https://hackertarget.com/tcpdump-examples/" == self.driver.current_url

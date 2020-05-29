from selenium.webdriver.common.by import By


class RegLocators:
    CREATE_ACCOUNT = (By.XPATH, '//div//a[@href="/reg"]')
    USERNAME_INPUT = (By.NAME, 'username')
    EMAIL_INPUT = (By.NAME, 'email')
    PASSWORD_INPUT = (By.NAME, 'password')
    PASSWORD_REPEAT_INPUT = (By.NAME, 'confirm')
    ACCEPT_CHECKBOX = (By.XPATH, '//input[contains(@name, "term")]')
    REG_BUTTON = (By.XPATH, '//input[contains(@value,"Register")]')
    LOG_IN = (By.XPATH, '//div//a[@href="/login"]')


class LoginLocators:
    CREATE_ACCOUNT = (By.XPATH, '//div//a[@href="/reg"]')
    USERNAME_INPUT = (By.NAME, 'username')
    PASSWORD_INPUT = (By.NAME, 'password')
    LOGIN_BUTTON = (By.XPATH, '//input[contains(@value,"Login")]')


class MainPageLocators:
    LOGOUT = (By.XPATH, '//div//a[@href="/logout"]')
    API_LOCATOR = (By.XPATH, '//div//a[@href="https://en.wikipedia.org/wiki/Application_programming_interface"]')
    INTERNET_LOCATOR = (By.XPATH, '//div//a[@href="https://www.popularmechanics.com/technology/infrastructure'
                                  '/a29666802/future-of-the-internet/"]')
    SMTP_LOCATOR = (By.XPATH, '//div//a[@href="https://ru.wikipedia.org/wiki/SMTP"]')
    PHRASE_LOCATOR = (By.XPATH, '//p[2]')
    PYTHON_LOCATOR = (By.XPATH, '//div//a[@href="https://www.python.org/"]')
    PYTHON_HISTORY = (By.XPATH, '//div//a[@href="https://en.wikipedia.org/wiki/History_of_Python"]')
    FLASK_LOCATOR = (By.XPATH, '//div//a[@href="https://flask.palletsprojects.com/en/1.1.x/#"]')
    LINUX_LOCATOR = (By.XPATH, '(//div//a[@href="javascript:"])[1]')
    NETWORK_LOCATOR = (By.XPATH, '(//div//a[@href="javascript:"])[2]')
    CENTOS_LOCATOR = (By.XPATH, '//div//a[@href="https://getfedora.org/ru/workstation/download/"]')
    NEWS_LOCATOR = (By.XPATH, '//div//a[@href="https://www.wireshark.org/news/"]')
    DOWNLOAD_LOCATOR = (By.XPATH, '//div//a[@href="https://www.wireshark.org/#download"]')
    EXAMPLES_LOCATOR = (By.XPATH, '//div//a[@href="https://hackertarget.com/tcpdump-examples/"]')



class CreateAdvert(LoginLocators):
    COMPANY_BUTTON = (By.XPATH, '//a[contains(@class, "center-module-campaigns")]')
    NEW_CAMPAIGN = (By.XPATH, ['//a[@href="/campaign/new" and contains(@class, "campaigns-tbl-settings")]',
                               '//div[contains(@class, "no-campaigns-msg")]//a'])
    AUDIO_ADVERT = (By.XPATH, '//div[contains(@class,"audiolistening")]')
    ADD_AUDIO = (By.XPATH, '//div[contains(@class,"input__file-wrap")]/input')
    ADD_ADVERT = (By.XPATH, '//div[contains(@class, "js-save-button-wrap")]/button')
    DONE = (By.XPATH, '//div[contains(@class, "icon-success")]')


class CreateSegment(LoginLocators):
    AUDITORY_BUTTON = (By.XPATH, '//a[@href="/segments"]')
    CREATE_SEGMENT = (
        By.XPATH, ['//a[@href="/segments/segments_list/new"]', '//button[contains(@class, "button button_submit")]'])
    ADD_SEGMENT = (By.XPATH, '//span[@data-translated="Add audience segments..."]')
    CHECKBOX = (By.XPATH, '//input[contains(@class, "source-checkbox")]')
    INPUT_NAME = (By.XPATH, '//div[@class="input input_create-segment-form"]//input[contains(@class, "input__inp")]')
    ADD_SEGMENT_FINAL = (By.XPATH, '//div[contains(@class, "js-add-button")]')
    DONE = (By.XPATH, '//div[contains(@class, "create-segment-form__btn-wrap")]/button')
    CHECK_IS_CREATED = (By.XPATH, '//table[contains(@class, "js-table")]')


class DeleteSegment(LoginLocators):
    DELETE_SEGMENT = (By.XPATH, '//button[contains(@class, "button_confirm-remove")]')
    CHECK_IS_CREATED = (By.XPATH, '//div[contains(@class, "js-modal-view-body")]')

    def detele_selected_segment(self, name):
        return By.XPATH, f'//a[contains(text(), "{name}")]//..//..//div[contains(@class, "remove-source-wrap")]'

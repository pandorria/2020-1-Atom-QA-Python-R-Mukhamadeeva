from selenium.webdriver.common.by import By


class LoginLocators:
    EMAIL_INPUT = (By.NAME, 'email')
    PASSWORD_INPUT = (By.NAME, 'password')
    COMEIN_BUTTON = (By.XPATH, '//div[contains(@class,"responseHead-module-button")]')
    LOGIN_BUTTON = (By.XPATH, '//div[contains(@class,"authForm-module-button")]')


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


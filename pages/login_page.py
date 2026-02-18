from selenium.webdriver.common.by import By
from configuration import BASE_URL_UI, LOGIN, PASSWORD


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = f"{BASE_URL_UI}/login"

        # Локаторы
        self.EMAIL_FIELD = (By.NAME, "login")
        self.PASS_FIELD = (By.NAME, "password")
        self.SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    def login(self):
        self.driver.get(self.url)
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(LOGIN)
        self.driver.find_element(*self.PASS_FIELD).send_keys(PASSWORD)
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

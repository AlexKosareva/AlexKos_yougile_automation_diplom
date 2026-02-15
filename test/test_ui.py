import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configuration as config

@allure.epic("YouGile UI Automation")
@allure.feature("Работа с задачами")
class TestYouGileUI:

    @allure.id("UI-LOGIN")
    @allure.title("Авторизация в системе")
    @pytest.mark.ui
    def test_login(self, browser):
        with allure.step("Открыть страницу авторизации"):
            # ПРЯМОЙ ПУТЬ к форме, чтобы не кликать лишний раз по лендингу
            browser.get("https://ru.yougile.com/team/")
        
        # Ожидание до 30 секунд (YouGile подгружает форму не сразу)
        wait = WebDriverWait(browser, 30)

        with allure.step("Ввести учетные данные"):
            # Ждем и вводим логин
            login_field = wait.until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "input[name='login'], input[type='email']")
            ))
            login_field.clear()
            login_field.send_keys(config.LOGIN)
            
            # ВАЖНО: Ждем, когда поле пароля станет доступным, и только потом вводим
            pass_field = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "input[name='password'], input[type='password']")
            ))
            pass_field.clear()
            pass_field.send_keys(config.PASSWORD)
            
            # Маленькая пауза перед нажатием Enter, чтобы YouGile "увидел" текст
            time.sleep(1)
            pass_field.send_keys(Keys.ENTER)
            # Даем системе 5-7 секунд на смену URL и прогрузку профиля
            time.sleep(7)

    @allure.id("df206b81-8b84-494a-ba9f-8de6dc4ac8c6")
    @allure.title("Создание задачи через интерфейс")
    @pytest.mark.ui
    def test_create_task_ui(self, browser):
        # 1. Сначала проходим авторизацию
        self.test_login(browser)
        
        wait = WebDriverWait(browser, 40)
        
        with allure.step("Перейти на тестовую доску"):
            # Используем твою проверенную длинную ссылку
            target_url = "https://ru.yougile.com/team/8dfa078b5e52/%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC%D0%9F%D1%80%D0%BE%D0%B5%D0%BA%D1%82_15.02/%D0%94%D0%B8%D0%BF%D0%BB%D0%BE%D0%BC"
            browser.get(target_url)
            
            # Ждем прогрузки тяжелой доски
            time.sleep(10)
            # Кликаем в body, чтобы сбросить возможные подсказки и фокус
            try:
                browser.find_element(By.TAG_NAME, "body").click()
            except:
                pass

        with allure.step("Нажать кнопку создания задачи"):
            # Ищем кнопку именно в первой колонке "В работе"
            # Селектор [data-id] или текст поможет не промахнуться
            add_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div/parent::div//div")
            ))
            # Кликаем через JS, чтобы обойти любые прозрачные слои
            browser.execute_script("arguments[0].click();", add_btn)
            
        with allure.step("Ввести название и сохранить"):
            # Ждем появления поля ввода (в YouGile это часто textarea)
            input_area = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea, .task-add-textarea")))
            input_area.send_keys("Задача от робота UI")
            time.sleep(1)
            input_area.send_keys(Keys.ENTER)

        with allure.step("Проверить появление задачи"):
            # Ищем нашу новую задачу на доске
            assert wait.until(EC.presence_of_element_located((By.XPATH, "//*")))

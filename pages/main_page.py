import allure
import time
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class YouGilePage:
    def __init__(self, browser: WebDriver):
        """Инициализация страницы. Принимает объект WebDriver."""
        self.browser = browser
        self.wait = WebDriverWait(browser, 40)

    @allure.step("Авторизация под пользователем: {email}")
    def login_manual(self, url: str, email: str, password: str) -> None:
        """Вход в систему. Принимает URL, логин и пароль (строки)."""
        with allure.step(f"Открыть страницу {url}"):
            self.browser.get(url)
            time.sleep(10)

        with allure.step("Ввести учетные данные"):
            selector = "input[type='email'], input[name='login']"
            login_field = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            self.browser.execute_script("arguments[0].click();", login_field)
            login_field.clear()
            login_field.send_keys(email)

            pass_selector = "input[type='password'], input[name='password']"
            pass_field = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, pass_selector))
            )
            pass_field.clear()
            pass_field.send_keys(password + Keys.ENTER)
            time.sleep(15)

    @allure.step("Перейти в проект '{project_name}'")
    def open_project(self, project_name: str) -> None:
        """Переход на доску проекта. Принимает имя проекта (строка)."""
        with allure.step("Найти плитку проекта и кликнуть по ней"):
            xpath = (
                f"//div[@data-testid='project-item']"
                f"//div[text()='{project_name}']"
            )
            project_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", project_btn
            )
            time.sleep(2)
            self.browser.execute_script("arguments[0].click();", project_btn)
            time.sleep(12)

    @allure.step("Создать задачу '{task_name}'")
    def create_task_visual(self, project_name: str, task_name: str) -> None:
        """Создание задачи. Принимает имя проекта и название задачи."""
        if project_name not in self.browser.title:
            self.open_project(project_name)

        with allure.step("Нажать '+ Добавить задачу'"):
            xpath_btn = "//span[contains(text(), 'Добавить задачу')]"
            btn = self.wait.until(
                EC.presence_of_element_located((By.XPATH, xpath_btn))
            )
            self.browser.execute_script("arguments[0].click();", btn)
            time.sleep(3)

        with allure.step(f"Ввести название '{task_name}'"):
            active_el = self.browser.switch_to.active_element
            active_el.send_keys(task_name)
            time.sleep(2)
            active_el.send_keys(Keys.ENTER)
            time.sleep(3)

    @allure.step("Проверить наличие задачи '{task_name}'")
    def check_task_exists(self, task_name: str) -> bool:
        """Проверка задачи. Возвращает логическое значение (True/False)."""
        with allure.step("Обновить страницу и найти задачу"):
            self.browser.refresh()
            time.sleep(15)
            xpath = (
                f"//div[contains(@class, 'task')]//*"
                f"[contains(text(), '{task_name}')]"
            )
            element = self.wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            is_found: bool = element.is_displayed()
            assert is_found, f"Задача {task_name} не найдена"
            return is_found

    @allure.step("Отправить сообщение в задачу '{task_name}'")
    def send_message(self, task_name: str, message_text: str) -> None:
        """Отправка сообщения. Принимает имя задачи и текст сообщения."""
        with allure.step(f"Открыть чат задачи {task_name}"):
            xpath = (
                f"//div[contains(@class, 'task')]//*"
                f"[contains(text(), '{task_name}')]"
            )
            self.wait.until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            ).click()
            time.sleep(4)

        with allure.step(f"Напечатать сообщение: {message_text}"):
            selector = "div[contenteditable='true'], .chat-input textarea"
            chat_input = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            chat_input.click()
            chat_input.send_keys(message_text)
            time.sleep(2)
            chat_input.send_keys(Keys.ENTER)
            time.sleep(3)
            body = self.browser.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)

    @allure.step("Изменить цвет задачи '{task_name}' на бирюзовый")
    def change_task_color(self, task_name: str) -> None:
        with allure.step(f"Открыть меню '...' на задаче {task_name}"):
            # СНАЧАЛА ЖДЕМ САМУ КАРТОЧКУ (чтобы она точно прогрузилась)
            card_xpath = (
                f"//*[text()='{task_name}']/ancestor::"
                "div[@data-testid='board-task-card']"
            )
            card = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, card_xpath))
            )

            # Сброс фокуса через ESCAPE
            body = self.browser.find_element(By.TAG_NAME, "body")
            body.send_keys(Keys.ESCAPE)
            time.sleep(2)

            # Теперь ищем точки внутри карточки
            dots_xpath = ".//div[@data-testid='board-task-menu']"
            dots = card.find_element(By.XPATH, dots_xpath)

            # Прокрутим к карточке, чтобы она была в центре
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", card
            )
            time.sleep(2)

            # Кликаем через JS
            self.browser.execute_script("arguments[0].click();", dots)
            time.sleep(3)

        with allure.step("Выбрать бирюзовый цвет"):
            color_xpath = "//div[contains(@class, 'bg-task-turquoise')]"
            # Ждем появления палитры
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, color_xpath))
            )
            colors = self.browser.find_elements(By.XPATH, color_xpath)
            # Берем именно ПОСЛЕДНИЙ открытый элемент палитры
            self.browser.execute_script("arguments[0].click();", colors[-1])
            time.sleep(3)

    @allure.step("Переименовать '{old_name}' в '{new_name}'")
    def rename_task_via_pencil(self, old_name: str, new_name: str) -> None:
        """Переименование. Принимает старое и новое имя задачи."""
        with allure.step(f"Найти карточку задачи '{old_name}'"):
            xpath = (
                f"//*[text()='{old_name}']/ancestor::"
                f"div[@data-testid='board-task-card']"
            )
            card = self.wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            ActionChains(self.browser).move_to_element(card).perform()
            time.sleep(2)

        with allure.step("Нажать на иконку карандаша"):
            pencil_xpath = ".//*[@data-testid='board-task-pancel']"
            pencil = card.find_element(By.XPATH, pencil_xpath)
            self.browser.execute_script("arguments[0].click();", pencil)
            time.sleep(2)

        with allure.step(f"Ввести новое название: {new_name}"):
            edit_field = self.browser.switch_to.active_element
            edit_field.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            edit_field.send_keys(Keys.BACKSPACE)
            time.sleep(1)
            edit_field.send_keys(new_name)
            time.sleep(2)
            edit_field.send_keys(Keys.ENTER)
            time.sleep(3)

    @allure.step("Удалить задачу '{task_name}'")
    def delete_task_direct(self, task_name: str) -> None:
        """Удаление. Принимает имя задачи."""
        with allure.step(f"Открыть меню '...' для задачи '{task_name}'"):
            xpath = (
                f"//*[text()='{task_name}']/ancestor::"
                f"div[@data-testid='board-task-card']"
                f"//div[@data-testid='board-task-menu']"
            )
            dots = self.wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            self.browser.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", dots
            )
            time.sleep(2)
            self.browser.execute_script("arguments[0].click();", dots)
            time.sleep(2)

        with allure.step("Выбрать 'Удалить' в выпадающем меню"):
            item_xpath = "//div[contains(text(), 'Удалить')]"
            delete_item = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, item_xpath))
            )
            self.browser.execute_script("arguments[0].click();", delete_item)
            time.sleep(2)

        with allure.step("Нажать на подтверждение"):
            confirm_xpath = (
                "//div[@role='button' and "
                "contains(@class, 'bg-action-attention')]"
            )
            confirm_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, confirm_xpath))
            )
            self.browser.execute_script("arguments[0].click();", confirm_btn)
            time.sleep(5)

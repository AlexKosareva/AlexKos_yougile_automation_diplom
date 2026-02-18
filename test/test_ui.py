import pytest
import allure
import time
import configuration as config
from pages.main_page import YouGilePage


@allure.epic("YouGile UI Automation")
@allure.feature("Атомарные тесты задач")
class TestYouGileUI:

    @pytest.fixture(autouse=True)
    def setup_page(self, browser):
        """Фикстура для инициализации страницы и авторизации."""
        self.page = YouGilePage(browser)
        # Проверяем авторизацию: если мы не на доске, логинимся
        if "yougile.com" not in browser.current_url:
            with allure.step("Первичная авторизация"):
                # ИЗМЕНЕНО: Добавлен config.BASE_URL_UI первым аргументом
                self.page.login_manual(
                    config.BASE_URL_UI,
                    config.LOGIN,
                    config.PASSWORD
                )
        else:
            with allure.step("Сброс состояния страницы перед новым тестом"):
                browser.refresh()
                time.sleep(5)

    @pytest.fixture
    def task_factory(self):
        """Фикстура-фабрика для создания задачи перед тестом."""
        def _create(name_prefix: str) -> str:
            task_name = f"{name_prefix}_{int(time.time())}"
            self.page.create_task_visual(config.PROJECT_NAME, task_name)
            return task_name
        return _create

    @allure.title("UI: Создание задачи")
    @pytest.mark.ui
    def test_create_task(self):
        task_name = f"Create_{int(time.time())}"
        self.page.create_task_visual(config.PROJECT_NAME, task_name)
        self.page.check_task_exists(task_name)

    @allure.title("UI: Отправка сообщения")
    @pytest.mark.ui
    def test_send_message(self, task_factory):
        task_name = task_factory("Chat")
        self.page.send_message(task_name, "Привет от автотеста!")

    @allure.title("UI: Смена цвета задачи")
    @pytest.mark.ui
    def test_change_task_color(self, task_factory):
        task_name = task_factory("Color")
        self.page.change_task_color(task_name)
        # Проверка внутри метода change_task_color уже есть

    @allure.title("UI: Переименование задачи")
    @pytest.mark.ui
    def test_rename_task(self, task_factory):
        task_name = task_factory("Rename")
        new_name = f"UPD_{task_name}"
        self.page.rename_task_via_pencil(task_name, new_name)
        self.page.check_task_exists(new_name)

    @allure.title("UI: Удаление задачи")
    @pytest.mark.ui
    def test_delete_task(self, task_factory):
        task_name = task_factory("Delete")
        self.page.delete_task_direct(task_name)

import requests
import pytest
import allure
import configuration as config


@allure.epic("YouGile API Automation")
@allure.feature("Задачи и колонки")
class TestYouGileAPI:

    @allure.id("354f480a-e5db-46c8-92ec-fd09ed3bd694")
    @allure.title("Создание новой колонки")
    @pytest.mark.api
    def test_create_column(self):
        headers = {
            "Authorization": f"Bearer {config.TOKEN}",
            "Content-Type": "application/json"
        }
        body = {
            "title": "Автотест: Колонка",
            "boardId": config.BOARD_ID
        }

        with allure.step("Отправить POST запрос на создание колонки"):
            url = f"{config.BASE_URL_API}columns"
            resp = requests.post(url, json=body, headers=headers)

        with allure.step("Проверить, что статус-код 201"):
            # Если падает с 404, выведем текст ошибки для диагностики
            assert resp.status_code == 201, f"Ошибка: {resp.text}"

    @allure.id("5211e343-8204-4f7c-9462-6e1d5e686d52")
    @allure.title("Создание задачи в колонке")
    @pytest.mark.api
    def test_create_task(self):
        headers = {
            "Authorization": f"Bearer {config.TOKEN}",
            "Content-Type": "application/json"
        }
        body = {
            "title": "Задача из автотеста",
            "columnId": config.COLUMN_ID
        }

        with allure.step("Отправить POST запрос на создание задачи"):
            url = f"{config.BASE_URL_API}tasks"
            resp = requests.post(url, json=body, headers=headers)

        with allure.step("Проверить статус-код 201"):
            assert resp.status_code == 201, f"Ошибка: {resp.text}"

    @allure.id("bb04aeae-0472-4a0a-9d6f-f5a05389ca9a")
    @allure.title("Получение списка задач")
    @pytest.mark.api
    def test_get_tasks_list(self):
        headers = {"Authorization": f"Bearer {config.TOKEN}"}
        params = {"columnId": config.COLUMN_ID}

        with allure.step("Отправить GET запрос на получение списка задач"):
            url = f"{config.BASE_URL_API}tasks"
            resp = requests.get(url, headers=headers, params=params)

        with allure.step("Проверить статус-код 200"):
            assert resp.status_code == 200

        with allure.step("Проверить формат ответа"):
            assert isinstance(resp.json().get("content"), list)

    @allure.id("dea5a86b-c8e3-4c3b-aa3d-4a8cf3f37a28")
    @allure.title("Негативный: создание задачи в несуществующей колонке")
    @pytest.mark.api
    def test_create_task_invalid_column(self):
        headers = {
            "Authorization": f"Bearer {config.TOKEN}",
            "Content-Type": "application/json"
        }
        body = {
            "title": "Fail Task",
            "columnId": "00000000-0000-0000-0000-000000000000"
        }

        with allure.step("Отправить запрос с несуществующим columnId"):
            url = f"{config.BASE_URL_API}tasks"
            resp = requests.post(url, json=body, headers=headers)

        with allure.step("Проверить, что сервер вернул ошибку 400 или 404"):
            # YouGile может вернуть 404 если объект не найден в БД
            assert resp.status_code in [400, 404]

    @allure.id("f2d8b845-2ffc-45eb-99ed-56649b8f72b8")
    @allure.title("Негативный: запрос задачи по невалидному ID")
    @pytest.mark.api
    def test_get_task_invalid_id(self):
        headers = {"Authorization": f"Bearer {config.TOKEN}"}

        with allure.step("Отправить GET запрос с невалидным ID"):
            url = f"{config.BASE_URL_API}tasks/invalid-id-format"
            resp = requests.get(url, headers=headers)

        with allure.step("Проверить наличие кода ошибки"):
            assert resp.status_code >= 400

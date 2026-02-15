import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def browser():
    options = Options()
    
    # СЕКРЕТНЫЙ ИНГРЕДИЕНТ: Скрываем от сайта, что браузером управляет робот
    # Это уберет плашку "Браузером управляет автоматизированное ПО" и поможет избежать 404
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Инициализация драйвера
    driver = webdriver.Chrome(options=options)
    
    # Еще одна настройка против обнаружения ботов
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    driver.maximize_window()
    driver.implicitly_wait(10) 
    
    yield driver
    
    # Закрытие браузера после теста
    driver.quit()

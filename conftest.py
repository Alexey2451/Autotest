import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os


@pytest.fixture(scope="session")
def driver():
    """Настройка WebDriver для всех тестов"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")

    # Для запуска в headless режиме раскомментируйте следующую строку:
    # chrome_options.add_argument("--headless")

    try:
        # Пытаемся установить ChromeDriver заново
        driver_path = ChromeDriverManager().install()
        print(f"ChromeDriver path: {driver_path}")

        # Проверяем, что файл существует и исполняем
        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"ChromeDriver not found at {driver_path}")

        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

    except Exception as e:
        print(f"Error with ChromeDriverManager: {e}")
        # Пытаемся использовать системный ChromeDriver
        try:
            service = Service()  # Использует системный PATH
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e2:
            print(f"Error with system ChromeDriver: {e2}")
            raise e2

    driver.implicitly_wait(10)
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def base_url():
    """Базовый URL для тестирования"""
    return "http://localhost"

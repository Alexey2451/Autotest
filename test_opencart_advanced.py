import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestOpenCartAdvanced:
    """Продвинутые автотесты для OpenCart"""

    def test_14_search_empty_query(self, driver, base_url):
        """Тест 14: Поиск с пустым запросом"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Находим поле поиска и отправляем пустой запрос
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "search")))
        search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-default, .btn-search, button.btn.btn-default")

        search_input.clear()
        search_button.click()

        time.sleep(2)

        # Проверяем обработку пустого поиска
        page_content = driver.page_source.lower()
        assert "search" in driver.current_url.lower() or "no results" in page_content or "найден" in page_content

    def test_15_search_special_characters(self, driver, base_url):
        """Тест 15: Поиск со специальными символами"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        search_input = wait.until(EC.presence_of_element_located((By.NAME, "search")))
        search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-default, .btn-search, button.btn.btn-default")

        # Тестируем поиск со специальными символами
        special_queries = ["<script>", "'; DROP TABLE", "café", "smartphone's"]

        for query in special_queries:
            search_input.clear()
            search_input.send_keys(query)
            search_button.click()
            time.sleep(1)

            # Проверяем, что страница не сломалась
            assert "error" not in driver.current_url.lower()

            # Возвращаемся на главную для следующего теста
            driver.get(base_url)
            search_input = wait.until(EC.presence_of_element_located((By.NAME, "search")))
            search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-default, .btn-search, button.btn.btn-default")

    def test_16_keyboard_navigation(self, driver, base_url):
        """Тест 16: Навигация с клавиатуры"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Проверяем навигацию по Tab
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "search")))
        search_input.click()

        # Используем Tab для перехода между элементами
        actions = ActionChains(driver)
        actions.send_keys(Keys.TAB).perform()
        time.sleep(0.5)

        # Проверяем, что фокус переместился
        focused_element = driver.switch_to.active_element
        assert focused_element != search_input

    def test_17_browser_back_forward(self, driver, base_url):
        """Тест 17: Функциональность кнопок Назад/Вперед браузера"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Переходим на другую страницу
        try:
            contact_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Contact")))
            contact_link.click()
            time.sleep(2)

            current_url = driver.current_url

            # Используем кнопку "Назад"
            driver.back()
            time.sleep(2)

            # Проверяем, что вернулись на главную
            assert driver.current_url != current_url

            # Используем кнопку "Вперед"
            driver.forward()
            time.sleep(2)

            # Проверяем, что вернулись на страницу контактов
            assert driver.current_url == current_url

        except (TimeoutException, NoSuchElementException):
            # Если нет ссылки на контакты, используем поиск
            search_input = driver.find_element(By.NAME, "search")
            search_input.send_keys("test")
            search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            search_button.click()
            time.sleep(2)

            driver.back()
            time.sleep(2)
            assert base_url in driver.current_url

    def test_18_page_refresh(self, driver, base_url):
        """Тест 18: Обновление страницы"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Запоминаем исходное состояние
        original_title = driver.title

        # Обновляем страницу
        driver.refresh()
        time.sleep(2)

        # Проверяем, что страница загрузилась корректно
        new_title = driver.title
        assert new_title == original_title

        # Проверяем наличие основных элементов
        logo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt*='Store'], .logo img, #logo img")))
        assert logo.is_displayed()

    def test_19_multiple_tabs(self, driver, base_url):
        """Тест 19: Работа с несколькими вкладками"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Запоминаем исходную вкладку
        original_window = driver.current_window_handle

        # Открываем новую вкладку
        driver.execute_script("window.open();")

        # Переключаемся на новую вкладку
        windows = driver.window_handles
        assert len(windows) == 2

        new_window = [window for window in windows if window != original_window][0]
        driver.switch_to.window(new_window)

        # Загружаем страницу в новой вкладке
        driver.get(base_url)
        time.sleep(2)

        # Проверяем, что страница загрузилась
        logo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt*='Store'], .logo img, #logo img")))
        assert logo.is_displayed()

        # Возвращаемся к исходной вкладке
        driver.switch_to.window(original_window)

        # Закрываем новую вкладку
        driver.switch_to.window(new_window)
        driver.close()
        driver.switch_to.window(original_window)

    def test_20_scroll_functionality(self, driver, base_url):
        """Тест 20: Функциональность прокрутки"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ждем загрузки страницы
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Прокручиваем вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Проверяем, что футер видим
        footer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "footer, .footer")))
        assert footer.is_displayed()

        # Прокручиваем вверх
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)

        # Проверяем, что шапка видима
        header = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "header, .header, nav")))
        assert header.is_displayed()

    def test_21_css_and_images_loading(self, driver, base_url):
        """Тест 21: Проверка загрузки CSS и изображений"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ждем загрузки страницы
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Проверяем загрузку изображений
        images = driver.find_elements(By.TAG_NAME, "img")
        loaded_images = 0

        for img in images[:5]:  # проверяем первые 5 изображений
            # Проверяем, что изображение загружено
            if driver.execute_script("return arguments[0].complete && arguments[0].naturalHeight !== 0", img):
                loaded_images += 1

        assert loaded_images > 0, "No images loaded successfully"

        # Проверяем применение CSS стилей
        body = driver.find_element(By.TAG_NAME, "body")
        background_color = body.value_of_css_property("background-color")

        # Проверяем, что CSS применился (цвет фона не прозрачный)
        assert background_color != "rgba(0, 0, 0, 0)"

    def test_22_form_validation(self, driver, base_url):
        """Тест 22: Валидация форм"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ищем любую форму на сайте (поиск, контакты, регистрация)
        try:
            # Сначала пробуем форму поиска
            search_form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form")))

            # Проверяем наличие обязательных полей
            required_fields = driver.find_elements(By.CSS_SELECTOR, "input[required], textarea[required]")

            if required_fields:
                # Пытаемся отправить форму с пустыми обязательными полями
                submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
                submit_button.click()
                time.sleep(1)

                # Проверяем, что валидация сработала (форма не отправилась или показала ошибку)
                validation_messages = driver.find_elements(By.CSS_SELECTOR, ".error, .invalid, .validation-error")

                # Если нативная HTML5 валидация, проверяем через JavaScript
                is_valid = driver.execute_script("return document.querySelector('form').checkValidity();")
                assert not is_valid or len(validation_messages) > 0

        except (TimeoutException, NoSuchElementException):
            print("No forms with validation found on this page")

    def test_23_error_handling(self, driver, base_url):
        """Тест 23: Обработка ошибок (404 страница)"""
        # Пытаемся перейти на несуществующую страницу
        driver.get(f"{base_url}/nonexistent-page-12345")

        time.sleep(2)

        # Проверяем обработку 404 ошибки
        page_content = driver.page_source.lower()

        # Ищем признаки 404 страницы
        error_indicators = ["404", "not found", "page not found", "не найдена", "ошибка"]
        found_error_indicator = any(indicator in page_content for indicator in error_indicators)

        # Или проверяем статус через JavaScript если возможно
        status_code = driver.execute_script("return window.performance.getEntriesByType('navigation')[0].responseStatus || 0")

        assert found_error_indicator or status_code == 404 or "error" in driver.current_url.lower()

    def test_24_javascript_functionality(self, driver, base_url):
        """Тест 24: Функциональность JavaScript"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Проверяем, что JavaScript работает
        js_enabled = driver.execute_script("return typeof jQuery !== 'undefined' || typeof $ !== 'undefined';")

        # Ждем загрузки страницы
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Проверяем интерактивные элементы
        try:
            # Ищем dropdown меню или другие интерактивные элементы
            dropdowns = driver.find_elements(By.CSS_SELECTOR, ".dropdown, .dropdown-toggle")

            if dropdowns:
                dropdown = dropdowns[0]

                # Наводим курсор или кликаем на dropdown
                actions = ActionChains(driver)
                actions.move_to_element(dropdown).perform()
                time.sleep(1)

                # Проверяем, что dropdown отреагировал
                dropdown_menu = driver.find_elements(By.CSS_SELECTOR, ".dropdown-menu, .dropdown-content")

                if dropdown_menu:
                    # Проверяем видимость меню
                    menu_visible = any(menu.is_displayed() for menu in dropdown_menu)
                    assert menu_visible or js_enabled

        except Exception as e:
            # Если нет dropdown элементов, просто проверяем базовую функциональность JS
            console_log_works = driver.execute_script("console.log('Test'); return true;")
            assert console_log_works

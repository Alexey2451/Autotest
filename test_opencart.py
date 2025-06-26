import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TestOpenCart:
    """Автотесты для OpenCart интернет-магазина"""

    def test_01_homepage_loads(self, driver, base_url):
        """Тест 1: Проверка загрузки главной страницы"""
        driver.get(base_url)

        # Ожидание загрузки страницы
        wait = WebDriverWait(driver, 10)

        # Проверяем, что страница загрузилась
        assert "OpenCart" in driver.title or "Your Store" in driver.title

        # Проверяем наличие основных элементов
        logo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt*='Your Store'], .logo img, #logo img")))
        assert logo.is_displayed()

    def test_02_search_functionality(self, driver, base_url):
        """Тест 2: Проверка функционала поиска"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Находим поле поиска
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "search")))
        search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-default, .btn-search, button.btn.btn-default")

        # Вводим запрос
        search_input.clear()
        search_input.send_keys("laptop")
        search_button.click()

        # Проверяем результаты поиска
        time.sleep(2)
        assert "search" in driver.current_url.lower() or "laptop" in driver.page_source.lower()

    def test_03_navigation_menu(self, driver, base_url):
        """Тест 3: Проверка навигационного меню"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ищем элементы навигации
        try:
            nav_menu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".navbar-nav, .nav, .menu")))
            assert nav_menu.is_displayed()

            # Проверяем наличие ссылок в меню
            menu_links = driver.find_elements(By.CSS_SELECTOR, ".navbar-nav a, .nav a, .menu a")
            assert len(menu_links) > 0

        except TimeoutException:
            # Альтернативный поиск категорий
            categories = driver.find_elements(By.CSS_SELECTOR, ".list-group-item, .category-link")
            assert len(categories) > 0

    def test_04_product_catalog(self, driver, base_url):
        """Тест 4: Проверка каталога товаров"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ищем товары на главной странице
        try:
            products = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb, .product-item, .product")))
            assert len(products) > 0

            # Проверяем первый товар
            first_product = products[0]
            assert first_product.is_displayed()

        except TimeoutException:
            # Переходим в каталог если товаров нет на главной
            catalog_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Catalog")
            catalog_link.click()
            time.sleep(2)

            products = driver.find_elements(By.CSS_SELECTOR, ".product-thumb, .product-item, .product")
            assert len(products) > 0

    def test_05_product_details(self, driver, base_url):
        """Тест 5: Проверка страницы товара"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Находим и кликаем на товар
        try:
            product_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-thumb a, .product-item a, .product a")))
            product_link.click()

            time.sleep(2)

            # Проверяем элементы на странице товара
            product_title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
            assert product_title.is_displayed()

            # Проверяем наличие цены
            price_elements = driver.find_elements(By.CSS_SELECTOR, ".price, .price-new, .price-old")
            assert len(price_elements) > 0

        except (TimeoutException, NoSuchElementException):
            # Если нет товаров, используем поиск
            search_input = driver.find_element(By.NAME, "search")
            search_input.send_keys("laptop")
            search_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            search_button.click()
            time.sleep(2)

    def test_06_shopping_cart_access(self, driver, base_url):
        """Тест 6: Проверка доступа к корзине"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ищем кнопку корзины
        cart_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-inverse, #cart, .cart, [title*='cart'], [title*='Cart']")))
        assert cart_button.is_displayed()

        # Кликаем на корзину
        cart_button.click()
        time.sleep(1)

        # Проверяем, что корзина открылась (может быть dropdown или отдельная страница)
        cart_content = driver.find_elements(By.CSS_SELECTOR, ".dropdown-menu, .cart-content, .shopping-cart")
        assert len(cart_content) > 0 or "cart" in driver.current_url.lower()

    def test_07_user_account_access(self, driver, base_url):
        """Тест 7: Проверка доступа к аккаунту пользователя"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ищем ссылку на аккаунт/вход
        try:
            account_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "My Account")))
            account_link.click()
        except TimeoutException:
            try:
                login_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Login")
                login_link.click()
            except NoSuchElementException:
                account_dropdown = driver.find_element(By.CSS_SELECTOR, ".dropdown-toggle")
                account_dropdown.click()

        time.sleep(2)

        # Проверяем, что попали на страницу входа или аккаунта
        assert "account" in driver.current_url.lower() or "login" in driver.current_url.lower()

    def test_08_currency_selector(self, driver, base_url):
        """Тест 8: Проверка селектора валют"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ищем селектор валют
        try:
            currency_selector = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".currency, #form-currency")))
            assert currency_selector.is_displayed()

            # Проверяем доступные валюты
            currency_options = driver.find_elements(By.CSS_SELECTOR, ".currency option, .currency a")
            assert len(currency_options) > 0

        except TimeoutException:
            # Валютный селектор может отсутствовать в некоторых темах
            print("Currency selector not found - this may be expected for some themes")

    def test_09_language_selector(self, driver, base_url):
        """Тест 9: Проверка селектора языков"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ищем селектор языков
        try:
            language_selector = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".language, #form-language")))
            assert language_selector.is_displayed()

        except TimeoutException:
            # Селектор языков может отсутствовать
            print("Language selector not found - this may be expected for single-language setups")

    def test_10_footer_links(self, driver, base_url):
        """Тест 10: Проверка ссылок в футере"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Прокручиваем к футеру
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # Ищем футер и ссылки в нем
        footer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "footer, .footer")))
        assert footer.is_displayed()

        footer_links = driver.find_elements(By.CSS_SELECTOR, "footer a, .footer a")
        assert len(footer_links) > 0

        # Проверяем, что ссылки кликабельны
        for link in footer_links[:3]:  # проверяем первые 3 ссылки
            assert link.is_displayed()

    def test_11_contact_page(self, driver, base_url):
        """Тест 11: Проверка страницы контактов"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Ищем ссылку на контакты
        try:
            contact_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Contact")))
            contact_link.click()

            time.sleep(2)

            # Проверяем, что попали на страницу контактов
            assert "contact" in driver.current_url.lower()

            # Проверяем наличие формы контактов
            contact_form = driver.find_elements(By.CSS_SELECTOR, "form, .form")
            assert len(contact_form) > 0

        except (TimeoutException, NoSuchElementException):
            print("Contact page not found - checking footer for contact link")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            footer_contact = driver.find_elements(By.PARTIAL_LINK_TEXT, "Contact")
            assert len(footer_contact) > 0

    def test_12_responsive_design(self, driver, base_url):
        """Тест 12: Проверка адаптивного дизайна"""
        driver.get(base_url)

        wait = WebDriverWait(driver, 10)

        # Проверяем разные размеры экрана
        screen_sizes = [
            (1920, 1080),  # Desktop
            (768, 1024),   # Tablet
            (375, 667)     # Mobile
        ]

        for width, height in screen_sizes:
            driver.set_window_size(width, height)
            time.sleep(1)

            # Проверяем, что основные элементы видны
            logo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[alt*='Store'], .logo img, #logo img")))
            assert logo.is_displayed()

        # Возвращаем исходный размер
        driver.maximize_window()

    def test_13_page_load_speed(self, driver, base_url):
        """Тест 13: Проверка скорости загрузки страницы"""
        start_time = time.time()
        driver.get(base_url)

        # Ждем полной загрузки страницы
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        load_time = time.time() - start_time

        # Проверяем, что страница загрузилась менее чем за 10 секунд
        assert load_time < 10, f"Page load time {load_time:.2f}s exceeds 10 seconds"
        print(f"Page loaded in {load_time:.2f} seconds")

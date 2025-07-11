# Автотесты для OpenCart

Этот проект содержит автотесты для локального сайта OpenCart, запущенного в Docker.

## Структура проекта

- `conftest.py` - настройки WebDriver и фикстуры для pytest
- `test_opencart.py` - основные автотесты (13 тестов)
- `test_opencart_advanced.py` - продвинутые автотесты (11 тестов)
- `requirements.txt` - зависимости Python
- `pytest.ini` - конфигурация pytest
- `reports/` - папка для HTML отчетов

## Установка и запуск

1. Активировать виртуальное окружение:
```bash
.venv\Scripts\activate
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Запустить все тесты:
```bash
pytest
```

4. Запустить тесты с HTML отчетом:
```bash
pytest --html=reports/report.html --self-contained-html
```

## Описание тестов

### Основные тесты (test_opencart.py):
1. Загрузка главной страницы
2. Функционал поиска
3. Навигационное меню
4. Каталог товаров
5. Страница товара
6. Доступ к корзине
7. Доступ к аккаунту пользователя
8. Селектор валют
9. Селектор языков
10. Ссылки в футере
11. Страница контактов
12. Адаптивный дизайн
13. Скорость загрузки страницы

### Продвинутые тесты (test_opencart_advanced.py):
14. Поиск с пустым запросом
15. Поиск со специальными символами
16. Навигация с клавиатуры
17. Кнопки Назад/Вперед браузера
18. Обновление страницы
19. Работа с несколькими вкладками
20. Функциональность прокрутки
21. Загрузка CSS и изображений
22. Валидация форм
23. Обработка ошибок (404 страница)
24. Функциональность JavaScript

## Требования

- Python 3.7+
- Google Chrome
- OpenCart запущен в Docker на localhost:80

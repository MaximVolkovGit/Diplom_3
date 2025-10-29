### Дипломный проект. Задание 3: Автотесты для UI
Автотесты для сервиса "Stellar Burger". Сайт: https://stellarburgers.education-services.ru
Тесты оптимизированы для проверки в браузерах Google Chrome и Mozilla Firefox

## Что сделано:

# Проверка основной функциональности

- переход по клику на «Конструктор»;
- переход по клику на раздел «Лента заказов»;
- если кликнуть на ингредиент, появится всплывающее окно с деталями;
- всплывающее окно закрывается кликом по крестику;
- при добавлении ингредиента в заказ счётчик этого ингредиента увеличивается.

# Раздел «Лента заказов»

- при создании нового заказа счётчик «Выполнено за всё время» увеличивается;
- при создании нового заказа счётчик «Выполнено за сегодня» увеличивается;
- после оформления заказа его номер появляется в разделе «В работе».

## Файлы:

- allure-results-chrome - каталог с отчетом о тестировании в Google Chrome
- allure-results-firefox - каталог с отчетом о тестировании в Mozilla Firefox

- data/ingredients.py - файл с данными ингредиентов
- data/urls - файл с URL сервиса и ручками
- data/user_data.py - файл с методами генерации данных для регистрации

- locators/locators.py - файл с локаторами элементов сервиса

- pages/base_page.py - файл с базовыми методами взаимодействия
- pages/login_page.py - файл с методами взаимодействия со страницей авторизации
- pages/main_page.py - файл с методами взаимодействия с главной страницей
- pages/order_feed_page.py - файл с методами взаимодействия со страницей ленты заказов

- tests/test_main_page.py - файл с проверками основного функционала
- tests/test_order_feed.py - файл с проверками ленты заказов

# Запуск в Chrome (по умолчанию)
pytest tests -v   

# Запуск в Firefox
pytest tests --browser=firefox -v   

# Запуск с отчётами в Chrome:
pytest --browser=chrome --alluredir=allure-results-chrome
allure serve allure-results-chrome

# Запуск с отчётами в Firefox:
pytest --browser=firefox --alluredir=allure-results-firefox
allure serve allure-results-firefox

# Создать общий отчет из обоих запусков
allure serve allure-results-chrome allure-results-firefox

# Перед работой с репозиторием требуется установить зависимости
pip install -r requirements.txt
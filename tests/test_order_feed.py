import pytest
import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

class TestOrderFeed:

    @allure.title('При создании нового заказа счётчик "Выполнено за всё время" увеличивается')
    @allure.description('''
    Проверка увеличения счетчика "Выполнено за всё время":
    1. Создать пользователя
    2. Перейти в ленту заказов  
    3. Запомнить начальное значение счетчика
    4. Создать заказ через UI
    5. Проверить что счетчик увеличился
    ''')
    def test_new_order_increases_total_counter(self, login_user, driver):
        # Создаем объекты страниц
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        # Переходим на страницу ленты заказов
        main_page.click_order_feed()
        
        # Ждем загрузки страницы
        assert order_feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась"
        
        # Получаем начальное значение счетчика
        initial_total = order_feed_page.get_total_orders_count()
        
        # Переходим обратно на главную страницу для создания заказа
        main_page.click_constructor()
        
        # Создаем заказ через UI и получаем финальный номер
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось создать заказ через UI"
        assert order_number != "9999", "Получен временный номер заказа 9999 вместо финального"
        
        # Переходим обратно в ленту заказов
        main_page.click_order_feed()
        
        # Ждем обновления счетчиков
        assert order_feed_page.wait_for_counters_update(initial_total, 0), "Счетчики не обновились"
        
        # Получаем новое значение счетчика
        new_total = order_feed_page.get_total_orders_count()
        
        # Проверяем, что счетчик увеличился
        assert new_total > initial_total, f"Счетчик 'Выполнено за все время' не увеличился. Было: {initial_total}, стало: {new_total}"

    @allure.title('При создании нового заказа счётчик "Выполнено за сегодня" увеличивается')
    @allure.description('''
    Проверка увеличения счетчика "Выполнено за сегодня":
    1. Создать пользователя
    2. Перейти в ленту заказов
    3. Запомнить начальное значение счетчика за сегодня
    4. Создать заказ через UI
    5. Проверить что дневной счетчик увеличился
    ''')
    def test_new_order_increases_today_counter(self, login_user, driver):
        # Создаем объекты страниц
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        # Переходим на страницу ленты заказов
        main_page.click_order_feed()
        
        # Ждем загрузки страницы
        assert order_feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась"
        
        # Получаем начальное значение счетчика за сегодня
        initial_today = order_feed_page.get_today_orders_count()
        
        # Переходим обратно на главную страницу для создания заказа
        main_page.click_constructor()
        
        # Создаем заказ через UI и получаем финальный номер
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось создать заказ через UI"
        assert order_number != "9999", "Получен временный номер заказа 9999 вместо финального"
        
        # Переходим обратно в ленту заказов
        main_page.click_order_feed()
        
        # Ждем обновления счетчиков
        assert order_feed_page.wait_for_counters_update(0, initial_today), "Счетчики не обновились"
        
        # Получаем новое значение счетчика за сегодня
        new_today = order_feed_page.get_today_orders_count()
        
        # Проверяем, что счетчик увеличился
        assert new_today > initial_today, f"Счетчик 'Выполнено за сегодня' не увеличился. Было: {initial_today}, стало: {new_today}"

    @allure.title('После оформления заказа его номер появляется в разделе "В работе"')
    @allure.description('''
    Проверка что номер заказа появляется в разделе "В работе":
    1. Создать пользователя
    2. Перейти в ленту заказов
    3. Создать заказ через UI
    4. Проверить что номер заказа появился в разделе "В работе"
    ''')
    def test_order_number_appears_in_progress(self, login_user, driver):
        # Создаем объекты страниц
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        
        # Переходим на страницу ленты заказов
        main_page.click_order_feed()
        
        # Ждем загрузки страницы
        assert order_feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась"
        
        # Переходим обратно на главную страницу для создания заказа
        main_page.click_constructor()
        
        # Создаем заказ через UI и получаем финальный номер
        order_number = main_page.create_order_ui()
        assert order_number is not None, "Не удалось создать заказ через UI"
        assert order_number != "9999", "Получен временный номер заказа 9999 вместо финального"
        
        # Переходим обратно в ленту заказов
        main_page.click_order_feed()
        
        # Ждем появления заказа в разделе "В работе" с нормализацией номеров
        normalized_order_number = order_feed_page.normalize_order_number(order_number)
        assert order_feed_page.wait_for_order_in_progress(normalized_order_number), f"Заказ {order_number} не появился в разделе 'В работе'"
        
        # Дополнительная проверка - получаем текущие заказы и проверяем наличие
        orders_in_progress_normalized = order_feed_page.get_orders_in_progress_normalized()
        
        assert normalized_order_number in orders_in_progress_normalized, (
            f"Заказ {order_number} (нормализованный: {normalized_order_number}) не найден в разделе 'В работе'."
            f"Текущие заказы: {orders_in_progress_normalized}"
        )
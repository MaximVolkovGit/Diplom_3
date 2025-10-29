import pytest
import requests
import allure
from data.urls import MainUrl, Endpoints
from data.ingredients import Ingredients
from pages.main_page import MainPage

class TestOrderFeed:

    @allure.title('При создании нового заказа счётчик "Выполнено за всё время" увеличивается')
    @allure.description('''
    Проверка увеличения счетчика "Выполнено за всё время":
    1. Создать пользователя
    2. Перейти в ленту заказов  
    3. Запомнить начальное значение счетчика
    4. Создать заказ через API
    5. Проверить что счетчик увеличился
    ''')
    def test_new_order_increases_total_counter(self, login_user, order_feed_page, create_new_user):
        # Получаем данные пользователя
        user_data, response = create_new_user
        
        # Переходим на страницу ленты заказов
        main_page = order_feed_page.driver 
        main_page = MainPage(main_page)
        main_page.click_order_feed()
        
        # Ждем загрузки страницы
        assert order_feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась"
        
        # Получаем начальное значение счетчика
        initial_total = order_feed_page.get_total_orders_count()
        
        # Создаем заказ через API
        token = response.json()["accessToken"]
        headers = {'Authorization': token}
        order_response = requests.post(
            MainUrl.MAIN_URL + Endpoints.CREATE_ORDER, 
            headers=headers, 
            json=Ingredients.correct_ingredients_data
        )
        
        assert order_response.status_code == 200, "Не удалось создать заказ"
        order_number = order_response.json()["order"]["number"]
        
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
    4. Создать заказ через API
    5. Проверить что дневной счетчик увеличился
    ''')
    def test_new_order_increases_today_counter(self, login_user, order_feed_page, create_new_user):
        # Получаем данные пользователя
        user_data, response = create_new_user
        
        # Переходим на страницу ленты заказов
        from pages.main_page import MainPage
        main_page = MainPage(order_feed_page.driver)
        main_page.click_order_feed()
        
        # Ждем загрузки страницы
        assert order_feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась"
        
        # Получаем начальное значение счетчика за сегодня
        initial_today = order_feed_page.get_today_orders_count()
        
        # Создаем заказ через API
        token = response.json()["accessToken"]
        headers = {'Authorization': token}
        order_response = requests.post(
            MainUrl.MAIN_URL + Endpoints.CREATE_ORDER, 
            headers=headers, 
            json=Ingredients.correct_ingredients_data
        )
        
        assert order_response.status_code == 200, "Не удалось создать заказ"
        
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
    3. Создать заказ через API
    4. Проверить что номер заказа появился в разделе "В работе"
    ''')
    def test_order_number_appears_in_progress(self, login_user, order_feed_page, create_new_user):
        # Получаем данные пользователя
        user_data, response = create_new_user
        
        # Переходим на страницу ленты заказов
        from pages.main_page import MainPage
        main_page = MainPage(order_feed_page.driver)
        main_page.click_order_feed()
        
        # Ждем загрузки страницы
        assert order_feed_page.is_order_feed_page_loaded(), "Страница ленты заказов не загрузилась"
        
        # Создаем заказ через API
        token = response.json()["accessToken"]
        headers = {'Authorization': token}
        order_response = requests.post(
            MainUrl.MAIN_URL + Endpoints.CREATE_ORDER, 
            headers=headers, 
            json=Ingredients.correct_ingredients_data
        )
        
        assert order_response.status_code == 200, "Не удалось создать заказ"
        order_number = order_response.json()["order"]["number"]
        
        # Ждем появления заказа в разделе "В работе" с нормализацией номеров
        assert order_feed_page.wait_for_order_in_progress(order_number), f"Заказ {order_number} не появился в разделе 'В работе'"
        
        # Дополнительная проверка - получаем текущие заказы и проверяем наличие
        orders_in_progress_normalized = order_feed_page.get_orders_in_progress_normalized()
        normalized_order_number = order_feed_page.normalize_order_number(order_number)
        
        assert normalized_order_number in orders_in_progress_normalized, (
            f"Заказ {order_number} (нормализованный: {normalized_order_number}) не найден в разделе 'В работе'."
            f"Текущие заказы: {orders_in_progress_normalized}"
        )
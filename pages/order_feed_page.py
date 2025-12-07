from pages.base_page import BasePage
from locators.locators import OrderFeedLocators
import allure

class OrderFeedPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('Проверить загрузку страницы ленты заказов')
    def is_order_feed_page_loaded(self):
        return self.is_element_visible(OrderFeedLocators.title_orders_list)

    @allure.step('Получить значение счетчика "Выполнено за все время"')
    def get_total_orders_count(self):
        try:
            counter = self.find_element(OrderFeedLocators.total_orders_counter)
            return int(counter.text) if counter.text else 0
        except:
            return 0

    @allure.step('Получить значение счетчика "Выполнено за сегодня"')
    def get_today_orders_count(self):
        try:
            counter = self.find_element(OrderFeedLocators.dayly_orders_counter)
            return int(counter.text) if counter.text else 0
        except:
            return 0

    @allure.step('Получить список номеров заказов в разделе "В работе"')
    def get_orders_in_progress(self):
        try:
            orders_elements = self.find_elements(OrderFeedLocators.number_order_in_job)
            return [order.text for order in orders_elements if order.text]
        except:
            return []

    @allure.step('Получить нормализованный список номеров заказов в разделе "В работе"')
    def get_orders_in_progress_normalized(self):
        try:
            orders_elements = self.find_elements(OrderFeedLocators.number_order_in_job)
            normalized_orders = []
            for order in orders_elements:
                if order.text:
                    # Убираем ведущие нули и преобразуем в число
                    normalized_orders.append(str(int(order.text)))
            return normalized_orders
        except:
            return []

    @allure.step('Нормализовать номер заказа')
    def normalize_order_number(self, order_number):
        if isinstance(order_number, str):
            # Убираем ведущие нули
            return str(int(order_number))
        else:
            return str(order_number)

    @allure.step('Ждать обновления счетчиков')
    def wait_for_counters_update(self, initial_total, initial_today, timeout=10):
        import time
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_total = self.get_total_orders_count()
            current_today = self.get_today_orders_count()
            if current_total > initial_total or current_today > initial_today:
                return True
        return False

    @allure.step('Ждать появления заказа в разделе "В работе"')
    def wait_for_order_in_progress(self, order_number, timeout=15):
        import time
        normalized_order = self.normalize_order_number(order_number)
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            orders_in_progress = self.get_orders_in_progress_normalized()
            if normalized_order in orders_in_progress:
                return True
        return False
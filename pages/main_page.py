from pages.base_page import BasePage
from locators.locators import MainPageLocators
from data.urls import MainUrl
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class MainPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.url = MainUrl.MAIN_URL

    @allure.step('Открыть главную страницу')
    def open(self):
        self.driver.get(self.url)
        self.wait_for_page_load()

    @allure.step('Кликнуть на кнопку "Конструктор"')
    def click_constructor(self):
        self.click_button(MainPageLocators.constructor_button)

    @allure.step('Кликнуть на кнопку "Лента заказов"')
    def click_order_feed(self):
        self.click_button(MainPageLocators.order_feed_button)

    @allure.step('Кликнуть на ингредиент')
    def click_ingredient(self):
        self.click_button(MainPageLocators.fluorescent_bun)

    @allure.step('Закрыть модальное окно ингредиента')
    def close_ingredient_modal(self):
        # Сначала пробуем закрыть крестиком
        try:
            self.click_button(MainPageLocators.close_ingredient_modal)
        except:
            # Если не получается, закрываем через оверлей или принудительно
            self.close_modal_by_overlay()

    @allure.step('Закрыть модальное окно кликом на оверлей')
    def close_modal_by_overlay(self):
        try:
            if self.is_element_visible(MainPageLocators.modal_overlay, timeout=2):
                self.click_button(MainPageLocators.modal_overlay)
        except:
            # Если не получается, используем принудительное закрытие
            self.force_close_modals()

    @allure.step('Проверить видимость модального окна')
    def is_ingredient_modal_visible(self):
        return self.is_element_visible(MainPageLocators.ingredient_modal)

    @allure.step('Проверить, что модальное окно закрыто')
    def is_ingredient_modal_closed(self):
        return self.is_element_not_visible(MainPageLocators.ingredient_modal)

    @allure.step('Перетащить ингредиент в конструктор')
    def drag_ingredient_to_constructor(self):
        self.close_all_modals()
        
        # Ждем появления элементов
        self.wait_element_visible(MainPageLocators.fluorescent_bun)
        self.wait_element_visible(MainPageLocators.constructor_drop_area)
        
        # Перетаскиваем ингредиент
        self.drag_and_drop(MainPageLocators.fluorescent_bun, MainPageLocators.constructor_drop_area)
        
    @allure.step('Получить значение счетчика ингредиента')
    def get_ingredient_counter(self):
        try:
            counter_element = self.find_element(MainPageLocators.ingredient_counter)
            
            if counter_element.is_displayed():
                counter_text = counter_element.text
                return int(counter_text) if counter_text else 0
                
            return 0
        except:
            return 0

    @allure.step('Закрыть все открытые модальные окна')
    def close_all_modals(self):
        try:
            # Пробуем закрыть крестиком
            if self.is_element_visible(MainPageLocators.close_ingredient_modal, timeout=1):
                self.click_button(MainPageLocators.close_ingredient_modal)
            
            # Пробуем закрыть через оверлей
            self.close_modal_by_overlay()
            
            # Принудительное закрытие как запасной вариант
            self.force_close_modals()
                
        except:
            self.force_close_modals()

    @allure.step('Создать заказ через UI')
    def create_order_ui(self):
        # Перетаскиваем ингредиент в конструктор
        self.drag_ingredient_to_constructor()
        
        # Нажимаем кнопку оформления заказа
        self.click_order_button()
        
        # Ждем появления модального окна с номером заказа
        order_number = self.get_order_number_from_modal()
        
        # Закрываем модальное окно заказа
        self.close_order_modal()
        
        return order_number

    @allure.step('Нажать кнопку оформления заказа')
    def click_order_button(self):
        self.click_button(MainPageLocators.order_button)

    @allure.step('Получить номер заказа из модального окна')
    def get_order_number_from_modal(self):
        try:
            # Ждем появления модального окна с номером заказа
            order_number_element = self.wait_element_visible(MainPageLocators.order_modal, timeout=10)
            return order_number_element.text
        except:
            return None

    @allure.step('Закрыть модальное окно заказа')
    def close_order_modal(self):
        try:
            self.click_button(MainPageLocators.close_order_modal)
        except:
            # Если не получается закрыть крестиком, закрываем через оверлей
            self.close_modal_by_overlay()

    @allure.step('Проверить, что кнопка оформления заказа доступна')
    def is_order_button_visible(self):
        return self.is_element_visible(MainPageLocators.order_button)
    
    @allure.step('Получить финальный номер заказа из модального окна')
    def get_final_order_number(self, timeout=15):
        try:
            # Сначала ждем, пока исчезнет временный номер 9999
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(MainPageLocators.order_number_loading)
            )
            
            # Затем получаем финальный номер заказа
            order_number_element = self.wait_element_visible(MainPageLocators.order_number_final, timeout=5)
            return order_number_element.text
        except Exception as e:
            # Если не удалось получить финальный номер, возвращаем None
            #print(f"Не удалось получить финальный номер заказа: {e}")
            return None

    @allure.step('Создать заказ через UI и получить финальный номер')
    def create_order_ui(self):
        """Создать заказ через пользовательский интерфейс и вернуть финальный номер"""
        # Перетаскиваем ингредиент в конструктор
        self.drag_ingredient_to_constructor()
        
        # Нажимаем кнопку оформления заказа
        self.click_order_button()
        
        # Ждем появления модального окна с номером заказа
        # Сначала может появиться 9999, поэтому ждем обновления
        order_number = self.get_final_order_number()
        
        # Закрываем модальное окно заказа
        self.close_order_modal()
        
        return order_number
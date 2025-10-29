from pages.base_page import BasePage
from locators.locators import MainPageLocators
from data.urls import MainUrl
import allure

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
                overlay = self.driver.find_element(*MainPageLocators.modal_overlay)
                overlay.click()
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
            # Ищем счетчик относительно ингредиента
            ingredient = self.driver.find_element(*MainPageLocators.fluorescent_bun)
            
            # Ищем родительский элемент ингредиента и в нем счетчик
            from selenium.webdriver.common.by import By
            parent = ingredient.find_element(By.XPATH, "./..")
            
            # Ищем счетчик внутри родительского элемента
            counter_elements = parent.find_elements(By.XPATH, ".//p[contains(@class, 'counter_counter__num__3nue1')]")
            
            if counter_elements and counter_elements[0].is_displayed():
                counter_text = counter_elements[0].text
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
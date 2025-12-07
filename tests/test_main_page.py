import pytest
import allure
from data.urls import MainUrl, URLS

class TestMainPage:

    @allure.title('Проверка перехода по клику на "Конструктор"')
    @allure.description('''
    Проверка навигации через кнопку "Конструктор":
    1. Открыть главную страницу
    2. Кликнуть по кнопке "Конструктор" в хедере
    3. Проверить, что текущий URL соответствует главной странице
    ''')
    def test_click_constructor_opens_main_page(self, main_page):
        main_page.click_constructor()
        current_url = main_page.get_current_url()
        assert current_url == MainUrl.MAIN_URL

    @allure.title('Проверка перехода по клику на "Лента заказов"')
    @allure.description('''
    Проверка навигации через кнопку "Лента заказов":
    1. Открыть главную страницу
    2. Кликнуть по кнопке "Лента заказов" в хедере
    3. Дождаться загрузки страницы
    4. Проверить, что текущий URL соответствует странице ленты заказов
    ''')
    def test_click_order_feed_opens_feed_page(self, main_page):
        main_page.click_order_feed()
        main_page.wait_for_page_load()
        current_url = main_page.get_current_url()
        expected_url = MainUrl.MAIN_URL + URLS.url_feed
        assert current_url == expected_url

    @allure.title('Проверка если кликнуть на ингредиент, появится всплывающее окно с деталями')
    @allure.description('''
    Проверка открытия модального окна с деталями ингредиента:
    1. Открыть главную страницу
    2. Кликнуть на ингредиент "Флюоресцентная булка R2-D3"
    3. Проверить, что модальное окно с деталями ингредиента открылось
    ''')
    def test_click_ingredient_opens_modal(self, main_page):
        """Клик на ингредиент открывает всплывающее окно с деталями"""
        main_page.click_ingredient()
        assert main_page.is_ingredient_modal_visible(), "Модальное окно не открылось"

    @allure.title('Проверка закрытия всплывающего окна по крестику')
    @allure.description('''
    Проверка закрытия модального окна через крестик:
    1. Открыть главную страницу
    2. Кликнуть на ингредиент "Флюоресцентная булка R2-D3"
    3. Проверить, что модальное окно открылось
    4. Кликнуть по крестику в правом верхнем углу модального окна
    5. Проверить, что модальное окно закрылось
    ''')
    def test_modal_closes_by_x_button(self, main_page):
        """Всплывающее окно закрывается кликом по крестику"""
        # Открываем модальное окно
        main_page.click_ingredient()
        assert main_page.is_ingredient_modal_visible(), "Модальное окно не открылось"
        
        # Закрываем модальное окно
        main_page.close_ingredient_modal()
        
        # Проверяем, что окно закрылось
        assert main_page.is_ingredient_modal_closed(), "Модальное окно не закрылось после клика по крестику"

    @allure.title('Увеличение счетчика ингредиента при перетаскивании его в корзину')
    @allure.description('''
    Проверка увеличения счетчика ингредиента при drag-and-drop:
    1. Открыть главную страницу
    2. Запомнить начальное значение счетчика у ингредиента
    3. Перетащить ингредиент "Флюоресцентная булка R2-D3" в область конструктора
    4. Проверить, что значение счетчика увеличилось
    ''')
    def test_drag_ingredient_increases_counter(self, main_page):
        """При перетаскивании ингредиента в корзину счётчик увеличивается"""
        # Получаем начальное значение счетчика
        initial_counter = main_page.get_ingredient_counter()
        
        # Перетаскиваем ингредиент в конструктор
        main_page.drag_ingredient_to_constructor()
        
        # Получаем новое значение счетчика
        new_counter = main_page.get_ingredient_counter()
        
        # Проверяем, что счетчик увеличился
        assert new_counter > initial_counter, f"Счетчик не увеличился. Было: {initial_counter}, стало: {new_counter}"
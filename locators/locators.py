from selenium.webdriver.common.by import By

class MainPageLocators:
    # Хедер и навигация
    constructor_button = (By.XPATH, "//p[text()='Конструктор']")                                    # Кнопка конструктор
    order_feed_button = (By.XPATH, "//p[text()='Лента Заказов']")                                   # Кнопка лента заказов
    personal_account_button = (By.XPATH, "//p[text()='Личный Кабинет']")                            # Кнопка личного кабинета
        
    # Модальное окно деталей ингредиента
    ingredient_modal = (By.XPATH, "//h2[text()= 'Детали ингредиента']")                             # Окно "Детали ингредиента"
    close_ingredient_modal = (By.XPATH, "//button[contains(@class,'close')]")                       # Крестик закрытия окна "Детали ингредиента"

    modal_overlay = (By.XPATH, "//div[contains(@class, 'Modal_modal_overlay__x2ZCr')]")              # Оверлей модального окна (важно для закрытия) 
    fluorescent_bun = (By.XPATH, "//img[@alt = 'Флюоресцентная булка R2-D3']")                       # блок Флюоресцентная булка R2-D3
    constructor_drop_area = (By.XPATH, "//div[contains(@class, 'constructor-element_pos_top')]")     # Область корзины для перетаскивания
    
    # Исправленный локатор для счетчика ингредиента
    ingredient_counter = (By.XPATH, "//img[@alt='Флюоресцентная булка R2-D3']/../..//p[contains(@class, 'counter_counter__num__3nue1')]")
    
    # Локаторы для создания заказа
    order_button = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")                       # Кнопка оформления заказа
    login_to_order_button = (By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]")             # Кнопка "Войти в аккаунт" (если не авторизован)
    
    order_modal = (By.XPATH, ".//h2[contains(@class, 'Modal_modal__title_shadow__3ikwq')]")    # Номер заказа в модальном окне
    order_number_loading = (By.XPATH, "//h2[text()='9999']")                                   # Временный номер заказа
    order_number_final = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title_shadow__3ikwq') and not(text()='9999')]")  # Финальный номер заказа
    close_order_modal = (By.XPATH, "//div[contains(@class, 'Modal_modal__')]//button[contains(@class, 'close')]")


class AuthPageLocators:
    """Форма авторизации"""

    auth_form = (By.XPATH, ".//div[@class = 'Auth_login__3hAey']")                                   # Форма авторизации
    email_input = (By.XPATH, ".//input[@name = 'name']")                                             # Поле ввода email
    password_input = (By.XPATH, ".//input[@name = 'Пароль']")                                        # Поле ввода пароля
    login_account_btn = (By.XPATH, "//button[text() = 'Войти']")                                     # Кнопка войти
    registration_btn = (By.XPATH, "//a[text() = 'Зарегистрироваться']")                              # Кнопка зерегистрироваться
    recover_btn = (By.XPATH, "//a[text() = 'Восстановить пароль']")                                  # Кнопка восстановить пароль


class OrderFeedLocators:
    """Форма Лента заказов"""

    title_orders_list = (By.XPATH, '//h1[text()="Лента заказов"]')                                   # Заголовок страницы
    orders_info = (By.XPATH, '//p[text()="Cостав"]')                                                 # Окно детали заказа
    total_orders_counter = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")  # Счетчик заказов за все время
    dayly_orders_counter = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")    # Счетчик заказов за сегодня
    number_order_in_job = (By.XPATH, ".//li[contains(@class, 'text_type_digits-default')]")          # Заказы "В работе"
    order_info_window = (By.XPATH, ".//li[contains(@class, 'OrderHistory_listItem__2x95r')][1]")     # 1 заказ в истории
    order_history = (By.XPATH, './/p[contains(@class, "text_type_digits-default")]')                 # Все заказы в истории
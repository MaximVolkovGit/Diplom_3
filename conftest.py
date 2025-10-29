import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from data.user_data import Person
from data.urls import MainUrl, Endpoints

def pytest_addoption(parser):
    """Опции для выбора браузера"""
    parser.addoption("--browser", default="chrome", help="Браузер: chrome или firefox")
    parser.addoption("--headless", action="store_true", help="Запуск в headless режиме")

@pytest.fixture
def driver(request):
    """Фикстура для создания и закрытия драйвера"""
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Браузер {browser_name} не поддерживается")
    
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(5)
    
    yield driver
    driver.quit()

@pytest.fixture
def main_page(driver):
    """Фикстура для главной страницы"""
    from pages.main_page import MainPage
    page = MainPage(driver)
    page.open()
    return page

@pytest.fixture
def user_data():
    """Фикстура для генерации данных пользователя"""
    return Person.create_data_correct_user()

@pytest.fixture
def create_new_user(user_data):
    """Фикстура для создания пользователя через API"""
    response = requests.post(MainUrl.MAIN_URL + Endpoints.CREATE_USER, json=user_data)
    
    yield user_data, response
    
    if response.status_code == 200:
        token = response.json()["accessToken"]
        headers = {'Authorization': token}
        requests.delete(MainUrl.MAIN_URL + Endpoints.DELETE_USER, headers=headers)

@pytest.fixture
def login_user(driver, create_new_user):
    """Фикстура для логина пользователя через UI"""
    user_data, response = create_new_user
    
    # Логин через UI
    from pages.login_page import LoginPage
    login_page = LoginPage(driver)
    login_page.open()
    
    # Добавляем дополнительную проверку и ожидание
    assert login_page.is_auth_form_visible(), "Форма авторизации не загрузилась"
    
    login_page.login(user_data["email"], user_data["password"])
    
    # Проверяем, что логин прошел успешно (перешли на главную страницу)
    import time
    time.sleep(0.5)  # Даем время для редиректа
    
    current_url = driver.current_url
    assert current_url == MainUrl.MAIN_URL, f"Логин не прошел успешно. Текущий URL: {current_url}"
    
    return user_data

@pytest.fixture
def order_feed_page(driver):
    """Фикстура для страницы ленты заказов"""
    from pages.order_feed_page import OrderFeedPage
    return OrderFeedPage(driver)
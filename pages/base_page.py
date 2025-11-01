from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import allure

class BasePage:

    def __init__(self, driver):
        self.driver = driver

    @allure.step('Получить текущий URL')
    def get_current_url(self):
        return self.driver.current_url

    @allure.step('Ждать кликабельности элемента')
    def wait_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    @allure.step('Ждать видимости элемента')
    def wait_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    @allure.step('Найти элемент с ожиданием')
    def find_element_with_wait(self, locator, timeout=10):
        return self.wait_element_visible(locator, timeout)

    @allure.step('Найти элемент без ожидания')
    def find_element(self, locator):
        return self.driver.find_element(*locator)

    @allure.step('Найти несколько элементов без ожидания')
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step('Кликнуть по кнопке')
    def click_button(self, locator, timeout=10):
        # Сначала пробуем стандартный клик
        try:
            element = self.wait_element_clickable(locator, timeout)
            element.click()
        except Exception as e:
            # Если возникает ошибка, пробуем JavaScript клик
            element = self.wait_element_visible(locator, timeout)
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step('Проверить видимость элемента')
    def is_element_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @allure.step('Проверить, что элемент невидим')
    def is_element_not_visible(self, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except:
            return False

    @allure.step('Принудительно закрыть все модальные окна')
    def force_close_modals(self):
        try:
            # Пробуем найти и закрыть любые модальные окна через ESC или клик по оверлею
            self.driver.execute_script("""
                // Закрыть модальные окна через ESC
                var escEvent = new KeyboardEvent('keydown', {
                    key: 'Escape',
                    code: 'Escape',
                    keyCode: 27,
                    which: 27
                });
                document.dispatchEvent(escEvent);
                
                // Кликнуть по любым оверлеям
                var overlays = document.querySelectorAll('[class*="overlay"], [class*="modal"]');
                overlays.forEach(function(overlay) {
                    if (overlay.style.display !== 'none') {
                        overlay.click();
                    }
                });
            """)
        except:
            pass

    @allure.step('Перетащить элемент')
    def drag_and_drop(self, source_locator, target_locator):
        source = self.find_element_with_wait(source_locator)
        target = self.find_element_with_wait(target_locator)
        
        # JavaScript реализация drag and drop
        self.driver.execute_script("""
            function createEvent(type) {
                var event = document.createEvent('CustomEvent');
                event.initCustomEvent(type, true, true, null);
                event.dataTransfer = {
                    data: {},
                    setData: function(type, val) {
                        this.data[type] = val;
                    },
                    getData: function(type) {
                        return this.data[type];
                    }
                };
                return event;
            }
            
            function dispatchEvent(element, event, transferData) {
                if (transferData !== undefined) {
                    event.dataTransfer = transferData;
                }
                if (element.dispatchEvent) {
                    element.dispatchEvent(event);
                } else if (element.fireEvent) {
                    element.fireEvent('on' + event.type, event);
                }
            }
            
            var source = arguments[0];
            var target = arguments[1];
            
            var dragStartEvent = createEvent('dragstart');
            dispatchEvent(source, dragStartEvent);
            
            var dragEnterEvent = createEvent('dragenter');
            dispatchEvent(target, dragEnterEvent);
            
            var dragOverEvent = createEvent('dragover');
            dispatchEvent(target, dragOverEvent);
            
            var dropEvent = createEvent('drop');
            dispatchEvent(target, dropEvent, dragStartEvent.dataTransfer);
            
            var dragEndEvent = createEvent('dragend');
            dispatchEvent(source, dragEndEvent, dragStartEvent.dataTransfer);
        """, source, target)

    @allure.step('Ждать загрузки страницы')
    def wait_for_page_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )

    @allure.step('Выполнить JavaScript код')
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)
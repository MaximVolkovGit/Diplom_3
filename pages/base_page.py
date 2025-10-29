from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def get_current_url(self):
        """Получить текущий URL"""
        return self.driver.current_url

    def wait_element_clickable(self, locator, timeout=10):
        """Ждать кликабельности элемента"""
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def wait_element_visible(self, locator, timeout=10):
        """Ждать видимости элемента"""
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def find_element_with_wait(self, locator, timeout=10):
        """Найти элемент с ожиданием"""
        return self.wait_element_visible(locator, timeout)

    def click_button(self, locator, timeout=10):
        """Кликнуть по кнопке"""
        # Сначала пробуем стандартный клик
        try:
            element = self.wait_element_clickable(locator, timeout)
            element.click()
        except Exception as e:
            # Если возникает ошибка, пробуем JavaScript клик
            element = self.wait_element_visible(locator, timeout)
            self.driver.execute_script("arguments[0].click();", element)

    def is_element_visible(self, locator, timeout=5):
        """Проверить видимость элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    def is_element_not_visible(self, locator, timeout=5):
        """Проверить, что элемент невидим"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except:
            return False

    def force_close_modals(self):
        """Принудительно закрыть все модальные окна"""
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

    def drag_and_drop(self, source_locator, target_locator):
        """Перетащить элемент с использованием JavaScript (работает в Firefox и Chrome)"""
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

    def wait_for_page_load(self, timeout=10):
        """Ждать загрузки страницы"""
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete'
        )
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def parse_imgur_with_selenium():
    options = Options()
    options.headless = True  # Запуск без GUI для экономии ресурсов
    
    # Дополнительные опции для подавления сообщений драйвера
    options.add_argument('--disable-gpu')  # Отключение GPU, рекомендуется для headless режима
    options.add_argument('--no-sandbox')   # Отключение песочницы
    options.add_argument('--disable-dev-shm-usage')  # Использование shared memory для уменьшения использования памяти
    options.add_argument('--log-level=3')  # Скрытие логов драйвера
    
    # Используем webdriver-manager для автоматического управления драйвером
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Переходим на страницу с последними загрузками
    driver.get('https://imgur.com/new/time')
    time.sleep(5)  # Ждем некоторое время, чтобы страница полностью загрузилась

    print("Page loaded with Selenium")
    
    # Прокрутка страницы вниз для загрузки большего количества изображений
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Прокрутка вниз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Ждем загрузки новой порции контента
        time.sleep(3)
        
        # Получаем новую высоту документа
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height

    # Обновленный селектор для нахождения ссылок на изображения
    image_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/gallery/"]')  # Пример селектора
    
    print(f"Found {len(image_elements)} image links")
    
    for i, element in enumerate(image_elements[:20]):
        image_url = element.get_attribute('href')
        print(f'Image {i+1}: {image_url}')
        time.sleep(0.1)  # Пауза между выводами
    
    driver.quit()

print("Поиск начался...")
parse_imgur_with_selenium()
print("Поиск завершен.")
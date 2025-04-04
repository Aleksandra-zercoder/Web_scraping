from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import csv
import time

# Настройки Firefox
firefox_options = Options()
# Окно можно открыть, если закомментировать следующую строку:
# firefox_options.add_argument('--headless')

# Используем дефолтный сервис, как в твоём рабочем коде
service = Service()
driver = webdriver.Firefox(service=service, options=firefox_options)

# Переход на сайт
url = "https://www.divan.ru/category/svet"
driver.get(url)

# Дадим JS подгрузить карточки
time.sleep(5)

# Поиск карточек
products = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-card"]')

# Сбор данных
results = []

for product in products:
    try:
        name = product.find_element(By.CSS_SELECTOR, 'div.lsooF span[itemprop="name"]').text.strip()
    except:
        name = None

    try:
        price = product.find_element(By.CSS_SELECTOR, 'span[data-testid="price"]').text.strip()
    except:
        price = None

    try:
        url = product.find_element(By.CSS_SELECTOR, 'div.lsooF a').get_attribute("href")
    except:
        url = None

    results.append({"name": name, "price": price, "url": url})

# Сохраняем в CSV
with open("products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "price", "url"])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Собрано и сохранено {len(results)} товаров в 'products.csv'")

# Закрываем драйвер
driver.quit()

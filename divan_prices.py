from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Настройки браузера
options = Options()
# options.add_argument("--headless")  # если не хочешь видеть окно

driver = webdriver.Firefox(service=Service(), options=options)
driver.get("https://www.divan.ru/category/divany")
time.sleep(3)

# 🔄 Автоскролл до конца страницы
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # ждём подгрузку
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Получаем все карточки
products = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-card"]')
print(f"🔍 Найдено карточек: {len(products)}")

results = []

for product in products:
    try:
        name = product.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]').text.strip()
    except:
        name = None

    try:
        # Актуальная цена (класс .KIkOH)
        price_element = product.find_element(By.CSS_SELECTOR, 'span[data-testid="price"].KIkOH')
        price_text = driver.execute_script("return arguments[0].childNodes[0].textContent;", price_element)
        price = int(price_text.replace(" ", "").replace("₽", ""))
    except:
        price = None

    try:
        # Старая цена (если есть)
        old_price_element = product.find_element(By.CSS_SELECTOR, 'span[data-testid="price"].SVNym')
        old_price_text = driver.execute_script("return arguments[0].childNodes[0].textContent;", old_price_element)
        old_price = int(old_price_text.replace(" ", "").replace("₽", ""))
    except:
        old_price = None  # если скидки нет

    try:
        link_element = product.find_element(By.CSS_SELECTOR, 'a[href*="/product/"]')
        href = link_element.get_attribute("href")
        url = "https://www.divan.ru" + href if href.startswith("/") else href
    except:
        url = None

    if name and price:
        results.append({
            "name": name,
            "price": price,
            "old_price": old_price if old_price else "",
            "url": url
        })

# Сохраняем в CSV
with open("sofas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "price", "old_price", "url"])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Сохранено {len(results)} диванов в 'sofas.csv'")

driver.quit()

# Анализ и график
df = pd.read_csv("sofas.csv")

if not df.empty:
    avg_price = df["price"].mean()
    print(f"📊 Средняя цена: {round(avg_price):,} ₽")

    # Гистограмма
    plt.hist(df["price"], bins=20, edgecolor='black')
    plt.title("Гистограмма цен на диваны")
    plt.xlabel("Цена, ₽")
    plt.ylabel("Количество")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("⚠️ Данные не найдены.")


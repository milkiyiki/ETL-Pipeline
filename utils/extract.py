from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime  # Tambahkan baris ini
import time

def extract_products(pages=50):
    products = []
    timestamp = datetime.now().isoformat()  # Gunakan datetime yang sudah diimpor

    try:
        driver = webdriver.Chrome()
        base_url = "https://fashion-studio.dicoding.dev/?page={}"

        for page in range(1, pages + 1):
            print(f"Scraping page {page}...") 
            driver.get(base_url.format(page))

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-title"))
            )

            titles = driver.find_elements(By.CLASS_NAME, "product-title")
            prices = driver.find_elements(By.CLASS_NAME, "product-price")
            ratings = driver.find_elements(By.CLASS_NAME, "product-rating")
            colors = driver.find_elements(By.CLASS_NAME, "product-colors")
            sizes = driver.find_elements(By.CLASS_NAME, "product-size")
            genders = driver.find_elements(By.CLASS_NAME, "product-gender")

            print(f"Found {len(titles)} titles, {len(prices)} prices, {len(ratings)} ratings.")  # Debugging: Check element counts

            for i in range(len(titles)):
                try:
                    product = {
                        "Title": titles[i].text.strip(),
                        "Price": prices[i].text.strip(),
                        "Rating": ratings[i].text.strip(),
                        "Colors": colors[i].text.strip(),
                        "Size": sizes[i].text.strip(),
                        "Gender": genders[i].text.strip(),
                        "Timestamp": timestamp
                    }
                    products.append(product)
                except IndexError:
                    print(f"Warning: Missing data on page {page}, product index {i}")
                    continue

            time.sleep(1)  # Delay kecil agar tidak overload server

    except Exception as e:
        print(f"[ERROR] Failed to extract data: {e}")

    finally:
        driver.quit()

    print(f"Extracted {len(products)} products.")  # Debugging: Check the number of extracted products
    return products

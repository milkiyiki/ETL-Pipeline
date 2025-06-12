import time
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetch_page_content(url):
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as error:
        print(f"Gagal mengambil data dari {url}: {error}")
        return None

def extract_fashion_item(item_block):
    try:
        title_elem = item_block.find('h3', class_='product-title')
        title = title_elem.text.strip() if title_elem else "Unknown Product"

        price_elem = item_block.find('div', class_='price-container')
        price_tag = price_elem.find('span', class_='price') if price_elem else item_block.find('p', class_='price')
        price = price_tag.text.strip() if price_tag else "Price Unavailable"

        # Default values
        rating, color, size, gender = "Invalid Rating", "", "", ""

        for p_tag in item_block.find_all('p'):
            lower_text = p_tag.text.lower()
            if "rating" in lower_text:
                rating = p_tag.text.strip()
            elif "colors" in lower_text:
                color = p_tag.text.strip()
            elif "size" in lower_text:
                size = p_tag.text.strip()
            elif "gender" in lower_text:
                gender = p_tag.text.strip()

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": color,
            "Size": size,
            "Gender": gender
        }

    except Exception as error:
        print(f"Gagal mengekstrak data produk: {error}")
        return {
            "Title": "Unknown Product",
            "Price": "Price Unavailable",
            "Rating": "Invalid Rating",
            "Colors": "",
            "Size": "",
            "Gender": ""
        }

def scrape_all_products(base_url='https://fashion-studio.dicoding.dev', start_page=1, delay=2):
    all_products = []
    current_page = start_page

    try:
        while True:
            page_url = base_url if current_page == 1 else base_url.format(current_page)
            print(f"Mengakses halaman: {page_url}")

            html_content = fetch_page_content(page_url)
            if not html_content:
                break

            soup = BeautifulSoup(html_content, "html.parser")
            product_sections = soup.find_all('div', class_='product-details')

            for section in product_sections:
                product_data = extract_fashion_item(section)
                all_products.append(product_data)

            next_btn = soup.find('li', class_='page-item next')
            if next_btn:
                current_page += 1
                time.sleep(delay)
            else:
                break

        return all_products

    except requests.exceptions.RequestException as error:
        print(f"Kesalahan HTTP saat scraping: {error}")
        return None
    except Exception as error:
        print(f"Kesalahan tak terduga saat scraping: {error}")
        return None

import sys
import os
from utils.extract import extract_products  # Memanggil extract_products
from utils.transform import transform_products
from utils.load import load_to_csv, load_to_gsheet, load_to_postgres
import datetime

# Menambahkan utils ke dalam path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils')))

def main():
    # Ekstraksi data dari website
    print("Extracting data...")
    raw_data = extract_products()  # Panggil extract_products untuk mengekstrak data

    print("Scraping page {page}...") # Debugging proses ekstrak

    print("Raw Data Extracted:", raw_data)  # Debugging: Cek data yang diekstrak
    
    # Periksa ekstraksi data
    print("Extracted Raw Data:", raw_data)

    # Menambah timestamp saat data diekstraksi
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for item in raw_data:
        item['timestamp'] = timestamp

    # Transformasi data
    print("Transforming data...")
    transformed_data = transform_products(raw_data)

    # Menyimpan data ke dalam CSV
    print("Loading data to CSV...")
    load_to_csv(transformed_data)

    # Menyimpan data ke Google Sheets
    print("Loading data to Google Sheets...")
    load_to_gsheet(transformed_data)

    # Menyimpan data ke PostgreSQL
    print("Loading data to PostgreSQL...")
    load_to_postgres(transformed_data)

    print("ETL process completed.")

if __name__ == "__main__":
    main()

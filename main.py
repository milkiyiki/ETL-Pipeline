from utils.extract import scrape_all_products
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import store_to_postgre, store_to_csv, store_to_sheets

def main():
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    all_fashion_data = scrape_all_products(BASE_URL)
    
    if all_fashion_data:
        try:
            print("✅ Scraping selesai. Jumlah produk:", len(all_fashion_data))
            df = transform_to_DataFrame(all_fashion_data)
            df = transform_data(df, 16000)

            print("✅ Transformasi data selesai.")
            db_url = 'postgresql+psycopg2://postgres:postgres@localhost:5432/fashiondb'
            
            print("✅ Menyimpan data ke CSV, PostgreSQL, dan Google Sheets...")
            store_to_csv(df)
            store_to_postgre(df, db_url)
            store_to_sheets(df)

            print("\n" + "-" * 20 + "\n")
            print(df.info())

        except Exception as e:
            print(f"❌ Terjadi kesalahan dalam proses: {e}")
    else:
        print("⚠️ Tidak ada data yang ditemukan.")

if __name__ == '__main__':
    main()

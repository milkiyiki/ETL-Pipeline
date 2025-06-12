from utils.extract import scrape_fashion
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import store_to_postgre, store_to_csv, store_to_sheets


def main():
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'
    EXCHANGE_RATE = 16000
    DB_URL = 'postgresql+psycopg2://postgres:postgres@localhost:5432/fashiondb'

    print("Memulai proses scraping...")
    all_fashion_data = scrape_fashion(BASE_URL)

    if not all_fashion_data:
        print("❌ Tidak ada data yang ditemukan.")
        return

    try:
        print("Transformasi data...")
        df = transform_to_DataFrame(all_fashion_data)
        df = transform_data(df, EXCHANGE_RATE)

        print("Menyimpan ke CSV...")
        store_to_csv(df)

        print("Menyimpan ke PostgreSQL...")
        store_to_postgre(df, DB_URL)

        print("Menyimpan ke Google Sheets...")
        store_to_sheets(df)

        print("\n✅ Pipeline ETL selesai!\n")
        print('-' * 40)
        print(df.info())

    except Exception as e:
        print(f"❌ Terjadi kesalahan dalam proses ETL: {e}")


if __name__ == '__main__':
    main()

import pandas as pd
from datetime import datetime

def transform_to_dataframe(data):
    try:
        return pd.DataFrame(data)
    except Exception as e:
        print(f"[DataFrame Creation] Gagal membuat DataFrame: {e}")
        return pd.DataFrame()

def transform_data(df, exchange_rate):
    required_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender']
    
    if not all(col in df.columns for col in required_columns):
        print("[Transform] DataFrame tidak memiliki semua kolom yang dibutuhkan.")
        return pd.DataFrame()
    
    try:
        # Tambah kolom timestamp
        df['Extraction_Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Filter invalid entries
        df = df[~df['Title'].str.contains("Unknown Product", na=False)]
        df = df[~df['Rating'].astype(str).str.contains("Invalid Rating", na=False)]
        df = df[~df['Price'].astype(str).str.contains("Price Unavailable", na=False)]

        # Bersihkan data
        df = df.drop_duplicates().dropna()

        # Transformasi kolom
        df['Price'] = df['Price'].replace(r'\$', '', regex=True).astype(float) * exchange_rate
        df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        df['Colors'] = df['Colors'].replace('Colors', '', regex=True).str.strip().astype(int)
        df['Size'] = df['Size'].replace('Size:', '', regex=True).str.strip()
        df['Gender'] = df['Gender'].replace('Gender:', '', regex=True).str.strip()

        # Pastikan tipe data sesuai
        df = df.astype({
            'Title': 'object',
            'Price': 'float64',
            'Rating': 'float64',
            'Colors': 'int64',
            'Size': 'object',
            'Gender': 'object',
            'Extraction_Timestamp': 'object'
        })

        return df
    
    except Exception as e:
        print(f"[Transform Error] Gagal mentransformasi data: {e}")
        return pd.DataFrame()

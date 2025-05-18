import csv
import gspread
import psycopg2
from oauth2client.service_account import ServiceAccountCredentials

def load_to_csv(data, filename='products.csv'):
    if not data:
        print("No data to write to CSV.")
        return
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def load_to_gsheet(data, creds_file='google-sheets-api.json', sheet_name='Products'):
    if not data:
        print("No data to upload to Google Sheets.")
        return
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
    client = gspread.authorize(creds)
    
    sheet = client.open(sheet_name).sheet1
    sheet.clear()
    sheet.insert_row(list(data[0].keys()), 1)
    for row in data:
        sheet.append_row(list(row.values()))

def load_to_postgres(data):
    if not data:
        print("No data to insert to PostgreSQL.")
        return
    conn = psycopg2.connect(
        dbname="your_db", user="your_user", password="your_password", host="localhost", port="5432"
    )
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            Title TEXT,
            Price FLOAT,
            Rating FLOAT,
            Colors TEXT,
            Size TEXT,
            Gender TEXT,
            timestamp TEXT
        );
    ''')
    for item in data:
        cur.execute('''
            INSERT INTO products (Title, Price, Rating, Colors, Size, Gender, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''', (
            item['Title'], item['Price'], item['Rating'], item['Colors'],
            item['Size'], item['Gender'], item['timestamp']
        ))
    conn.commit()
    cur.close()
    conn.close()

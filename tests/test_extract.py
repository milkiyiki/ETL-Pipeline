import unittest
from utils.extract import extract_products

class TestExtract(unittest.TestCase):
    def test_extract_products(self):
        result = extract_products(pages=2)  # Sesuaikan jumlah halaman sesuai kebutuhan
        self.assertIsInstance(result, list)  # Pastikan hasilnya adalah list
        self.assertGreater(len(result), 0)  # Pastikan ada data yang diambil
        self.assertIn('Title', result[0])  # Pastikan data produk memiliki key 'Title'
        self.assertIn('Price', result[0])  # Pastikan data produk memiliki key 'Price'

if __name__ == "__main__":
    unittest.main()
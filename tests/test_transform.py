import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.transform import transform_products

class TestTransform(unittest.TestCase):
    def test_no_nulls(self):
        raw_data = [{
            "Title": "Shirt",
            "Price": "$10",
            "Rating": "4.5",
            "Colors": "3 Colors",
            "Size": "Size: M",
            "Gender": "Gender: Male",
            "timestamp": "2024-05-14 10:00:00"
        }]
        result = transform_products(raw_data)
        for item in result:
            self.assertNotIn(None, item.values())

if __name__ == '__main__':
    unittest.main()

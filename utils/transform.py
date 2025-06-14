import unittest
import pandas as pd
from utils.transform import transform_to_dataframe, transform_data

class TransformFunctionalityTests(unittest.TestCase):

    def setUp(self):
        self.raw_data = [
            {
                "Title": "Product A",
                "Price": "$10.00",
                "Rating": "Rating: ⭐ 4.5 / 5",
                "Colors": "3 Colors",
                "Size": "Size: M",
                "Gender": "Gender: Men"
            },
            {
                "Title": "Unknown Product",
                "Price": "Price Unavailable",
                "Rating": "Invalid Rating",
                "Colors": "",
                "Size": "",
                "Gender": ""
            }
        ]

    def test_dataframe_creation(self):
        df = transform_to_dataframe(self.raw_data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertIn("Title", df.columns)

    def test_data_transformation(self):
        df = transform_to_dataframe(self.raw_data)
        transformed_df = transform_data(df, exchange_rate=16000)

        self.assertEqual(len(transformed_df), 1)

        self.assertTrue(pd.api.types.is_float_dtype(transformed_df["Price"]))
        self.assertTrue(pd.api.types.is_float_dtype(transformed_df["Rating"]))
        self.assertTrue(pd.api.types.is_integer_dtype(transformed_df["Colors"]))
        self.assertIn("Extraction_Timestamp", transformed_df.columns)

        self.assertEqual(transformed_df.iloc[0]["Title"], "Product A")
        self.assertEqual(transformed_df.iloc[0]["Size"], "M")
        self.assertEqual(transformed_df.iloc[0]["Gender"], "Men")

if __name__ == "__main__":
    unittest.main()

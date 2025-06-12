import unittest
import pandas as pd
from utils.transform import transform_to_DataFrame, transform_data

class DataTransformTests(unittest.TestCase):

    def setUp(self):
        self.sample_df = pd.DataFrame({
            'Title': ['Product A', 'Unknown Product', 'Product B', 'Product C'],
            'Price': ['$10.00', '$20.00', 'Price Unavailable', '$15.00'],
            'Rating': ['4.5/5', 'Invalid Rating', '4.0/5', '5.0/5'],
            'Colors': ['3 Colors', '2 Colors', '4 Colors', '3 Colors'],
            'Size': ['Size: M', 'Size: L', 'Size: XL', 'Size: S'],
            'Gender': ['Gender: Male', 'Gender: Female', 'Gender: Male', 'Gender: Unisex']
        })
        self.usd_to_local = 1.1

    def test_dataframe_conversion(self):
        result_df = transform_to_DataFrame(self.sample_df)

        self.assertIsInstance(result_df, pd.DataFrame, "Expected output type is DataFrame")

        for column in ["Title", "Price", "Rating", "Colors", "Size", "Gender"]:
            self.assertIn(column, result_df.columns, f"{column} column should exist")

    def test_data_cleaning_transformation(self):
        cleaned_df = transform_data(self.sample_df, self.usd_to_local)

        self.assertIn("Extraction Timestamp", cleaned_df.columns, "Timestamp column missing after transformation")

        self.assertNotIn("Unknown Product", cleaned_df["Title"].values, "Unknown products should be excluded")

        self.assertNotIn("Invalid Rating", cleaned_df["Rating"].values, "Invalid ratings must be filtered")

        self.assertNotIn("Price Unavailable", cleaned_df["Price"].values, "Unavailable prices must be removed")

        self.assertEqual(
            len(cleaned_df), len(cleaned_df.drop_duplicates()),
            "No duplicate rows should remain"
        )

        self.assertFalse(cleaned_df.isnull().values.any(), "DataFrame should not contain any null values")

        self.assertAlmostEqual(cleaned_df["Price"].iloc[0], 10.0 * self.usd_to_local)

        self.assertEqual(cleaned_df["Rating"].iloc[0], 4.5)
        self.assertEqual(cleaned_df["Colors"].iloc[0], 3)
        self.assertEqual(cleaned_df["Size"].iloc[0], "M")
        self.assertEqual(cleaned_df["Gender"].iloc[0], "Male")

    def test_handle_empty_input(self):
        empty_input = pd.DataFrame()
        transformed_empty = transform_data(empty_input, self.usd_to_local)
        self.assertTrue(transformed_empty.empty, "Transformed result should be empty when input is empty")

if __name__ == "__main__":
    unittest.main()

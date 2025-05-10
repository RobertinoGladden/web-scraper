import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):
    def test_transform_success(self):
        df = pd.DataFrame({
            'Title': ['Product1'],
            'Price': ['100'],
            'Rating': ['4.5 / 5'],
            'Colors': ['3 Colors'],
            'Size': ['Size: M'],
            'Gender': ['Gender: Men'],
            'timestamp': ['2025-05-05'],
            'page_number': [1]
        })
        result = transform_data(df)
        self.assertFalse(result.empty, "DataFrame should not be empty")
        self.assertEqual(result['Price'].iloc[0], 1600000.0)  # 100 USD * 16000
        self.assertEqual(result['Rating'].iloc[0], 4.5)
        self.assertEqual(result['Colors'].iloc[0], 3)
        self.assertEqual(result['Size'].iloc[0], 'M')
        self.assertEqual(result['Gender'].iloc[0], 'Men')

    def test_transform_empty_df(self):
        df = pd.DataFrame()
        result = transform_data(df)
        self.assertTrue(result.empty, "Empty DataFrame should remain empty")

    def test_transform_invalid_price(self):
        df = pd.DataFrame({
            'Title': ['Product1'],
            'Price': ['invalid'],
            'Rating': ['4.5 / 5'],
            'Colors': ['3 Colors'],
            'Size': ['Size: M'],
            'Gender': ['Gender: Men'],
            'timestamp': ['2025-05-05'],
            'page_number': [1]
        })
        result = transform_data(df)
        self.assertTrue(result.empty, "DataFrame with invalid price should be filtered out")

    def test_transform_price_unavailable(self):
        df = pd.DataFrame({
            'Title': ['Product1'],
            'Price': ['Price Unavailable'],
            'Rating': ['4.5 / 5'],
            'Colors': ['3 Colors'],
            'Size': ['Size: M'],
            'Gender': ['Gender: Men'],
            'timestamp': ['2025-05-05'],
            'page_number': [1]
        })
        result = transform_data(df)
        self.assertTrue(result.empty, "DataFrame with 'Price Unavailable' should be filtered out")

    def test_transform_invalid_colors(self):
        df = pd.DataFrame({
            'Title': ['Product1'],
            'Price': ['100'],
            'Rating': ['4.5 / 5'],
            'Colors': ['Invalid Colors'],
            'Size': ['Size: M'],
            'Gender': ['Gender: Men'],
            'timestamp': ['2025-05-05'],
            'page_number': [1]
        })
        result = transform_data(df)
        self.assertTrue(result.empty, "DataFrame with invalid colors should be filtered out")

    def test_transform_invalid_rating(self):
        df = pd.DataFrame({
            'Title': ['Product1'],
            'Price': ['100'],
            'Rating': ['Invalid Rating'],
            'Colors': ['3 Colors'],
            'Size': ['Size: M'],
            'Gender': ['Gender: Men'],
            'timestamp': ['2025-05-05'],
            'page_number': [1]
        })
        result = transform_data(df)
        self.assertFalse(result.empty, "DataFrame with invalid rating should set rating to 0")
        self.assertEqual(result['Rating'].iloc[0], 0.0)

    def test_transform_duplicates(self):
        df = pd.DataFrame({
            'Title': ['Product1', 'Product1'],
            'Price': ['100', '100'],
            'Rating': ['4.5 / 5', '4.5 / 5'],
            'Colors': ['3 Colors', '3 Colors'],
            'Size': ['Size: M', 'Size: M'],
            'Gender': ['Gender: Men', 'Gender: Men'],
            'timestamp': ['2025-05-05', '2025-05-05'],
            'page_number': [1, 1]
        })
        result = transform_data(df)
        self.assertEqual(len(result), 1, "Duplicates should be removed")

    def test_transform_null_values(self):
        df = pd.DataFrame({
            'Title': [None],
            'Price': ['100'],
            'Rating': ['4.5 / 5'],
            'Colors': ['3 Colors'],
            'Size': ['Size: M'],
            'Gender': ['Gender: Men'],
            'timestamp': ['2025-05-05'],
            'page_number': [1]
        })
        result = transform_data(df)
        self.assertTrue(result.empty, "DataFrame with null Title should be filtered out")

    def test_transform_empty_size_gender(self):
        df = pd.DataFrame({
            'Title': ['Product1'],
            'Price': ['100'],
            'Rating': ['4.5 / 5'],
            'Colors': ['3 Colors'],
            'Size': [''],
            'Gender': [''],
            'timestamp': ['2025-05-05'],
            'page_number': [1]
        })
        result = transform_data(df)
        self.assertTrue(result.empty, "DataFrame with empty Size or Gender should be filtered out")

    def test_transform_null_rating(self):
        df = pd.DataFrame({
            'Title': ['Product1'],
            'Price': ['100'],
            'Rating': [None],
            'Colors': ['3 Colors'],
            'Size': ['Size: M'],
            'Gender': ['Gender: Men'],
            'timestamp': ['2025-05-05'],
            'page_number': [1]
        })
        result = transform_data(df)
        self.assertFalse(result.empty, "DataFrame with null Rating should set rating to 0")
        self.assertEqual(result['Rating'].iloc[0], 0.0)

if __name__ == '__main__':
    unittest.main()
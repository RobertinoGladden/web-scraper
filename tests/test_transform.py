import unittest
from utils.transform import transform_data
import pandas as pd
from unittest.mock import patch

class TestTransform(unittest.TestCase):
    def test_transform_data_not_empty(self):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': ['100'], 'Rating': ['4.5 / 5'], 'Colors': ['3 Colors'], 'Size': ['Size: M'], 'Gender': ['Gender: Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        df_transformed = transform_data(df)
        self.assertFalse(df_transformed.empty, "Transformed DataFrame should not be empty")
    
    def test_transform_price_conversion(self):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': ['100'], 'Rating': ['4.5 / 5'], 'Colors': ['3 Colors'], 'Size': ['Size: M'], 'Gender': ['Gender: Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        df_transformed = transform_data(df)
        self.assertEqual(df_transformed['Price'].iloc[0], 1600000.0, "Price should be converted to 1600000.0")

    def test_transform_empty_dataframe(self):
        df = pd.DataFrame()
        result = transform_data(df)
        self.assertTrue(result.empty, "Empty DataFrame should return empty")

    def test_transform_invalid_price(self):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': ['invalid'], 'Rating': ['4.5 / 5'], 'Colors': ['3 Colors'], 'Size': ['Size: M'], 'Gender': ['Gender: Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        result = transform_data(df)
        self.assertFalse(result.empty, "DataFrame with invalid price should be handled")
        self.assertEqual(result['Price'].iloc[0], 0.0, "Invalid price should be set to 0")

    def test_transform_price_unavailable(self):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': ['Price Unavailable'], 'Rating': ['4.5 / 5'], 'Colors': ['3 Colors'], 'Size': ['Size: M'], 'Gender': ['Gender: Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        result = transform_data(df)
        self.assertFalse(result.empty, "DataFrame with 'Price Unavailable' should be handled")
        self.assertEqual(result['Price'].iloc[0], 0.0, "Price Unavailable should be converted to 0")

    def test_transform_invalid_rating(self):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': ['100'], 'Rating': ['Invalid Rating'], 'Colors': ['3 Colors'], 'Size': ['Size: M'], 'Gender': ['Gender: Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        result = transform_data(df)
        self.assertFalse(result.empty, "DataFrame with invalid rating should set rating to 0")
        self.assertEqual(result['Rating'].iloc[0], 0.0, "Invalid rating should be set to 0")

    def test_transform_invalid_colors(self):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': ['100'], 'Rating': ['4.5 / 5'], 'Colors': ['Invalid Colors'], 'Size': ['Size: M'], 'Gender': ['Gender: Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        result = transform_data(df)
        self.assertFalse(result.empty, "DataFrame with invalid colors should set colors to 0")
        self.assertEqual(result['Colors'].iloc[0], 0, "Invalid colors should be set to 0")

    def test_transform_null_title(self):
        df = pd.DataFrame({'Title': [None], 'Price': ['100'], 'Rating': ['4.5 / 5'], 'Colors': ['3 Colors'], 'Size': ['Size: M'], 'Gender': ['Gender: Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        result = transform_data(df)
        self.assertTrue(result.empty, "DataFrame with null title should be filtered out")

    def test_transform_exception_handling(self):
        with patch('pandas.DataFrame.dropna', side_effect=Exception("Unexpected error")):
            df = pd.DataFrame({'Title': ['Product1'], 'Price': ['100'], 'Rating': ['4.5 / 5'], 'Colors': ['3 Colors'], 'Size': ['Size: M'], 'Gender': ['Gender: Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
            result = transform_data(df)
            self.assertTrue(result.empty, "DataFrame should be empty on unexpected error")

if __name__ == '__main__':
    unittest.main()
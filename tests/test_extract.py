import unittest
from utils.extract import scrape_data
import pandas as pd
from unittest.mock import patch, MagicMock
import requests

class TestExtract(unittest.TestCase):
    @patch('requests.get')
    def test_scrape_data_success(self, mock_get):
        # Simulate only one page with a product
        mock_response = MagicMock()
        mock_response.text = """
        <html>
        <body>
            <div class="collection-card">
                <h3 class="product-title">Test Product</h3>
                <span class="price">$100</span>
                <p style="font-size: 14px; color: #777;">Rating: ⭐ 4.5 / 5</p>
                <p style="font-size: 14px; color: #777;">3 Colors</p>
                <p style="font-size: 14px; color: #777;">Size: M</p>
                <p style="font-size: 14px; color: #777;">Gender: Men</p>
            </div>
        </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()

        mock_empty_response = MagicMock()
        mock_empty_response.text = "<html><body></body></html>"
        mock_empty_response.raise_for_status = MagicMock()

        mock_get.side_effect = [mock_response] + [mock_empty_response] * 49

        df = scrape_data()
        self.assertFalse(df.empty, "DataFrame should not be empty for valid product")
        self.assertEqual(len(df), 1, "Should scrape one product")
        self.assertEqual(df['Title'].iloc[0], "Test Product")
        self.assertEqual(df['Price'].iloc[0], 100.0)
        self.assertEqual(df['Rating'].iloc[0], "4.5 / 5")
        self.assertEqual(df['Colors'].iloc[0], "3 Colors")
        self.assertEqual(df['Size'].iloc[0], "M")
        self.assertEqual(df['Gender'].iloc[0], "Men")

    @patch('requests.get')
    def test_scrape_data_request_failure(self, mock_get):
        mock_get.side_effect = requests.RequestException("Mocked request failure")
        df = scrape_data()
        self.assertTrue(df.empty, "DataFrame should be empty on request failure")

    @patch('requests.get')
    def test_scrape_data_no_products(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body></body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        df = scrape_data()
        self.assertTrue(df.empty, "DataFrame should be empty when no products are found")

    @patch('requests.get')
    def test_scrape_data_invalid_product(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = """
        <html>
        <body>
            <div class="collection-card">
                <p style="font-size: 14px; color: #777;">Rating: Not Rated</p>
            </div>
        </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        df = scrape_data()
        self.assertTrue(df.empty, "DataFrame should be empty for invalid product with missing critical fields")

    @patch('requests.get')
    def test_scrape_data_columns(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = """
        <html>
        <body>
            <div class="collection-card">
                <h3 class="product-title">Test Product</h3>
                <span class="price">$100</span>
                <p style="font-size: 14px; color: #777;">Rating: ⭐ 4.5 / 5</p>
                <p style="font-size: 14px; color: #777;">3 Colors</p>
                <p style="font-size: 14px; color: #777;">Size: M</p>
                <p style="font-size: 14px; color: #777;">Gender: Men</p>
            </div>
        </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        df = scrape_data()
        expected_columns = {'Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'timestamp', 'page_number'}
        self.assertEqual(set(df.columns), expected_columns, "Columns should match expected set")

    @patch('requests.get')
    def test_scrape_data_attribute_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = """
        <html>
        <body>
            <div class="collection-card">
                <h3>Invalid</h3> <!-- Simulate missing product-title class -->
            </div>
        </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        df = scrape_data()
        self.assertTrue(df.empty, "DataFrame should be empty on AttributeError")

    @patch('requests.get')
    def test_scrape_data_invalid_price_format(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = """
        <html>
        <body>
            <div class="collection-card">
                <h3 class="product-title">Test Product</h3>
                <span class="price">invalid_price</span>
                <p style="font-size: 14px; color: #777;">Rating: ⭐ 4.5 / 5</p>
                <p style="font-size: 14px; color: #777;">3 Colors</p>
                <p style="font-size: 14px; color: #777;">Size: M</p>
                <p style="font-size: 14px; color: #777;">Gender: Men</p>
            </div>
        </body>
        </html>
        """
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        df = scrape_data()
        self.assertTrue(df.empty, "DataFrame should be empty for invalid price format")

if __name__ == '__main__':
    unittest.main()
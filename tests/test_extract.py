import unittest
from utils.extract import scrape_data
import pandas as pd
import requests
from unittest.mock import patch, MagicMock

class TestExtract(unittest.TestCase):
    def test_scrape_data_not_empty(self):
        df = scrape_data()
        if df.empty:
            self.skipTest("Skipping test: DataFrame is empty, possibly due to website inaccessibility.")
        self.assertFalse(df.empty, "DataFrame should not be empty")
    
    def test_scrape_data_columns(self):
        df = scrape_data()
        if df.empty:
            self.skipTest("Skipping test: DataFrame is empty, possibly due to website inaccessibility.")
        expected_columns = {'Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'timestamp', 'page_number'}
        self.assertEqual(set(df.columns), expected_columns, "Columns should match expected set")

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
        self.assertFalse(df.empty, "Should handle products with missing fields")
        self.assertEqual(df['Title'].iloc[0], "Untitled Product", "Should set default title")
        self.assertEqual(df['Rating'].iloc[0], "0.0 / 5", "Should set default rating for Not Rated")

    @patch('requests.get')
    def test_scrape_data_log_html(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "<html><body><p>Test HTML</p></body></html>"
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        with self.assertLogs('utils.extract', level='INFO') as log:
            df = scrape_data()
            self.assertIn("Scraping page 1", log.output[0])

if __name__ == '__main__':
    unittest.main()
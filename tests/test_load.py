import unittest
import pandas as pd
from utils.load import save_to_csv, save_to_google_sheets
from unittest.mock import patch, MagicMock
import logging
import gspread

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger('utils.load')
        self.logger.setLevel(logging.INFO)
        self.handler = logging.StreamHandler()
        self.logger.addHandler(self.handler)
    
    def tearDown(self):
        self.logger.removeHandler(self.handler)

    def test_save_to_csv_success(self):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': [1600000.0], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            save_to_csv(df, 'test.csv')
            mock_to_csv.assert_called_once_with('test.csv', index=False)

    def test_save_to_csv_failure_empty_df(self):
        df = pd.DataFrame()
        with self.assertRaises(ValueError):
            save_to_csv(df, 'test.csv')

    def test_save_to_csv_failure_exception(self):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': [1600000.0], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        with patch('pandas.DataFrame.to_csv', side_effect=Exception("CSV write error")):
            with self.assertRaises(Exception):
                save_to_csv(df, 'test.csv')

    @patch('gspread.authorize')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_save_to_google_sheets_success_existing(self, mock_creds, mock_authorize):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': [1600000.0], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        
        mock_client.open.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        mock_worksheet.clear.return_value = None
        mock_worksheet.update.return_value = None
        mock_authorize.return_value = mock_client
        
        save_to_google_sheets(df, 'Test_Sheet')
        mock_client.open.assert_called_once_with('Test_Sheet')
        mock_spreadsheet.get_worksheet.assert_called_once_with(0)
        mock_worksheet.clear.assert_called_once()
        mock_worksheet.update.assert_called_once()

    @patch('gspread.authorize')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_save_to_google_sheets_create_new(self, mock_creds, mock_authorize):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': [1600000.0], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        
        mock_client.open.side_effect = gspread.SpreadsheetNotFound
        mock_client.create.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        mock_worksheet.clear.return_value = None
        mock_worksheet.update.return_value = None
        mock_authorize.return_value = mock_client
        
        save_to_google_sheets(df, 'Test_Sheet')
        mock_client.create.assert_called_once_with('Test_Sheet')
        mock_spreadsheet.get_worksheet.assert_called_once_with(0)
        mock_worksheet.update.assert_called_once()

    @patch('gspread.authorize')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_save_to_google_sheets_failure_empty_df(self, mock_creds, mock_authorize):
        df = pd.DataFrame()
        with self.assertRaises(ValueError):
            save_to_google_sheets(df, 'Test_Sheet')

    @patch('gspread.authorize')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_save_to_google_sheets_share_failure(self, mock_creds, mock_authorize):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': [1600000.0], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        
        mock_response = MagicMock()
        mock_response.json.return_value = {'error': {'code': 400, 'message': 'Share error'}}
        
        mock_client.open.side_effect = gspread.SpreadsheetNotFound
        mock_client.create.return_value = mock_spreadsheet
        mock_spreadsheet.share.side_effect = gspread.exceptions.APIError(mock_response)
        mock_authorize.return_value = mock_client
        
        with self.assertRaises(gspread.exceptions.APIError):
            save_to_google_sheets(df, 'Test_Sheet')

    @patch('gspread.authorize')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_save_to_google_sheets_share_fallback(self, mock_creds, mock_authorize):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': [1600000.0], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        
        mock_client.open.side_effect = gspread.SpreadsheetNotFound
        mock_client.create.return_value = mock_spreadsheet
        mock_spreadsheet.share.side_effect = AttributeError("Share attribute error")
        mock_spreadsheet.client.insert_permission.return_value = None
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        mock_worksheet.clear.return_value = None
        mock_worksheet.update.return_value = None
        mock_authorize.return_value = mock_client
        
        save_to_google_sheets(df, 'Test_Sheet')
        mock_spreadsheet.client.insert_permission.assert_called_once()

    @patch('gspread.authorize')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_save_to_google_sheets_clear_failure(self, mock_creds, mock_authorize):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': [1600000.0], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        
        mock_response = MagicMock()
        mock_response.json.return_value = {'error': {'code': 400, 'message': 'Clear error'}}
        
        mock_client.open.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        mock_worksheet.clear.side_effect = gspread.exceptions.APIError(mock_response)
        mock_authorize.return_value = mock_client
        
        with self.assertRaises(gspread.exceptions.APIError):
            save_to_google_sheets(df, 'Test_Sheet')

    @patch('gspread.authorize')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_save_to_google_sheets_update_failure(self, mock_creds, mock_authorize):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': [1600000.0], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_worksheet = MagicMock()
        
        mock_response = MagicMock()
        mock_response.json.return_value = {'error': {'code': 400, 'message': 'Update error'}}
        
        mock_client.open.return_value = mock_spreadsheet
        mock_spreadsheet.get_worksheet.return_value = mock_worksheet
        mock_worksheet.clear.return_value = None
        mock_worksheet.update.side_effect = gspread.exceptions.APIError(mock_response)
        mock_authorize.return_value = mock_client
        
        with self.assertRaises(gspread.exceptions.APIError):
            save_to_google_sheets(df, 'Test_Sheet')

    @patch('gspread.authorize')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_save_to_google_sheets_share_fallback_failure(self, mock_creds, mock_authorize):
        df = pd.DataFrame({'Title': ['Product1'], 'Price': [1600000.0], 'Rating': [4.5], 'Colors': [3], 'Size': ['M'], 'Gender': ['Men'], 'timestamp': ['2025-05-05'], 'page_number': [1]})
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        
        mock_client.open.side_effect = gspread.SpreadsheetNotFound
        mock_client.create.return_value = mock_spreadsheet
        mock_spreadsheet.share.side_effect = AttributeError("Share attribute error")
        mock_spreadsheet.client.insert_permission.side_effect = Exception("Insert permission failed")
        mock_authorize.return_value = mock_client
        
        with self.assertRaises(Exception):
            save_to_google_sheets(df, 'Test_Sheet')

if __name__ == '__main__':
    unittest.main()
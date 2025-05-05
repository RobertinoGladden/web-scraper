import pandas as pd
import logging
import gspread
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_to_csv(df, file_path):
    """
    Saves the DataFrame to a CSV file.
    """
    try:
        if df.empty:
            raise ValueError("Input DataFrame is empty.")
        
        df.to_csv(file_path, index=False)
        logger.info(f"Data saved to CSV: {file_path}")
    
    except Exception as e:
        logger.error(f"Failed to save CSV: {str(e)}")
        raise

def save_to_google_sheets(df, spreadsheet_name):
    """
    Saves the DataFrame to a Google Sheet using google-auth.
    """
    try:
        if df.empty:
            raise ValueError("Input DataFrame is empty.")
        
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.file'
        ]
        creds = Credentials.from_service_account_file('google-sheets-api.json', scopes=scopes)
        client = gspread.authorize(creds)
        
        try:
            spreadsheet = client.open(spreadsheet_name)
            logger.info(f"Found existing spreadsheet: {spreadsheet_name}")
        except gspread.SpreadsheetNotFound:
            spreadsheet = client.create(spreadsheet_name)
            logger.info(f"Created new spreadsheet: {spreadsheet_name}")
        
        try:
            spreadsheet.share(None, perm_type='anyone', role='writer', notify=False)
            logger.info(f"Shared spreadsheet with 'Anyone with the link' as editor. URL: {spreadsheet.url}")
        except gspread.exceptions.APIError as e:
            logger.error(f"API error while sharing spreadsheet: {str(e)}")
            raise
        except AttributeError as e:
            logger.error(f"Attribute error while sharing spreadsheet: {str(e)}")
            try:
                permissions = {
                    'type': 'anyone',
                    'role': 'writer'
                }
                spreadsheet.client.insert_permission(spreadsheet.id, permissions)
                logger.info(f"Shared spreadsheet using legacy method. URL: {spreadsheet.url}")
            except Exception as e:
                logger.error(f"Failed to share using legacy method: {str(e)}")
                raise
        
        worksheet = spreadsheet.get_worksheet(0)
        
        try:
            worksheet.clear()
        except gspread.exceptions.APIError as e:
            logger.error(f"Failed to clear worksheet: {str(e)}")
            raise
        
        try:
            worksheet.update([df.columns.values.tolist()] + df.values.tolist())
            logger.info(f"Data saved to Google Sheet: {spreadsheet_name}. URL: {spreadsheet.url}")
        except gspread.exceptions.APIError as e:
            logger.error(f"Failed to update worksheet: {str(e)}")
            raise
    
    except gspread.exceptions.APIError as e:
        logger.error(f"Google Sheets API error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Failed to save to Google Sheets: {str(e)}")
        raise
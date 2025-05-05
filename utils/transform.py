import pandas as pd
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transform_data(df):
    """
    Transforms the scraped data by cleaning and converting to appropriate data types.
    Converts Price from USD to IDR (1 USD = 16000 IDR).
    Returns the transformed DataFrame.
    """
    try:
        if df.empty:
            logger.warning("Input DataFrame is empty. Skipping transformation.")
            return df
        
        logger.info("Starting transformation...")
        
        initial_len = len(df)
        logger.info(f"Initial records: {initial_len}")
        
        df = df.dropna(subset=['Title']) 
        logger.info(f"After removing null Title: {len(df)} records remain.")
        
        df['Price'] = df['Price'].replace("Price Unavailable", "0")
        df['Price'] = df['Price'].apply(lambda x: "0" if not str(x).replace('.', '').isdigit() else x)
        
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
        
        df['Price'] = df['Price'] * 16000
        
        def extract_rating(rating_str):
            match = re.search(r'(\d+\.\d+|\d+)\s*/\s*5', rating_str)
            return float(match.group(1)) if match else 0.0
        
        df['Rating'] = df['Rating'].apply(extract_rating)
        logger.info(f"After processing Rating: {len(df)} records remain.")
        
        def extract_colors(colors_str):
            match = re.search(r'(\d+)\s*Colors?', colors_str)
            return int(match.group(1)) if match else 0
        
        df['Colors'] = df['Colors'].apply(extract_colors)
        
        df['Size'] = df['Size'].str.replace('Size: ', '')
        df['Gender'] = df['Gender'].str.replace('Gender: ', '')
        
        df['Price'] = df['Price'].astype(float)
        df['Rating'] = df['Rating'].astype(float)
        df['Colors'] = df['Colors'].astype(int)
        df['Size'] = df['Size'].astype(str)
        df['Gender'] = df['Gender'].astype(str)
        df['timestamp'] = df['timestamp'].astype(str)
        df['page_number'] = df['page_number'].astype(int)
        
        logger.info("Data types ensured.")
        
        logger.info(f"Transformed {len(df)} records.")
        return df
    
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}")
        return pd.DataFrame()
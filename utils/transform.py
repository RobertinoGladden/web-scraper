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
        
        # Remove null or invalid titles
        df = df.dropna(subset=['Title'])
        df = df[~df['Title'].str.lower().isin(['unknown product', ''])]
        logger.info(f"After removing invalid Title: {len(df)} records remain.")
        
        # Handle price
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0)
        df = df[df['Price'] > 0]  # Remove products with invalid or zero price
        df['Price'] = df['Price'] * 16000  # Convert to IDR
        
        # Extract rating as float
        def extract_rating(rating_str):
            match = re.search(r'(\d+\.\d+|\d+)\s*/\s*5', rating_str)
            return float(match.group(1)) if match else 0.0
        
        df['Rating'] = df['Rating'].apply(extract_rating)
        df = df[df['Rating'] >= 0]  # Ensure valid rating
        
        # Extract colors as integer
        def extract_colors(colors_str):
            match = re.search(r'(\d+)\s*Colors?', colors_str)
            return int(match.group(1)) if match else 0
        
        df['Colors'] = df['Colors'].apply(extract_colors)
        df = df[df['Colors'] > 0]  # Remove invalid colors
        
        # Clean Size and Gender
        df['Size'] = df['Size'].str.replace('Size: ', '').str.strip()
        df['Gender'] = df['Gender'].str.replace('Gender: ', '').str.strip()
        df = df[(df['Size'] != '') & (df['Gender'] != '')]  # Remove empty Size or Gender
        
        # Remove duplicates based on Title
        df = df.drop_duplicates(subset=['Title'], keep='first')
        logger.info(f"After removing duplicates: {len(df)} records remain.")
        
        # Ensure data types
        df['Price'] = df['Price'].astype(float)
        df['Rating'] = df['Rating'].astype(float)
        df['Colors'] = df['Colors'].astype(int)
        df['Size'] = df['Size'].astype(str)
        df['Gender'] = df['Gender'].astype(str)
        df['timestamp'] = df['timestamp'].astype(str)
        df['page_number'] = df['page_number'].astype(int)
        
        # Final validation
        if df.isnull().any().any():
            logger.warning("Null values found after transformation.")
            df = df.dropna()
        
        if len(df) == 0:
            logger.warning("No valid data after transformation.")
            return pd.DataFrame()
        
        logger.info(f"Transformed {len(df)} records.")
        return df
    
    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}")
        return pd.DataFrame()
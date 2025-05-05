import logging
from utils.extract import scrape_data
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Main function to run the ETL pipeline.
    """
    try:
        logger.info("Starting extraction...")
        df = scrape_data()
        if df.empty:
            raise ValueError("No data extracted from the website.")
        
        logger.info("Starting transformation...")
        df_transformed = transform_data(df)
        if df_transformed.empty:
            raise ValueError("No data after transformation.")
        
        logger.info("Starting loading...")
        save_to_csv(df_transformed, "products.csv")
        save_to_google_sheets(df_transformed, "ETL_Pipeline_Results")
        
        logger.info("ETL pipeline completed successfully.")
    
    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
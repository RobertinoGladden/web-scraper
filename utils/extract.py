import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_data():
    """
    Scrapes data from fashion-studio.dicoding.dev across all pages.
    Returns a DataFrame with Title, Price, Rating, Colors, Size, Gender, timestamp, and page_number.
    """
    try:
        all_data = []
        pages_scraped = 0
        products_scraped = 0
        
        for page in range(1, 51):
            if page == 1:
                url = "https://fashion-studio.dicoding.dev/"
            else:
                url = f"https://fashion-studio.dicoding.dev/page{page}"
            logger.info(f"Scraping page {page}: {url}")
            
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
                }
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                logger.info(f"Response status code: {response.status_code}")
                
                soup = BeautifulSoup(response.text, 'html.parser')
                products = soup.select('.collection-card')
                if not products:
                    logger.warning(f"No products found on page {page}. Selector '.collection-card' may be incorrect.")
                    continue
                
                logger.info(f"Found {len(products)} products on page {page}")
                
                for idx, product in enumerate(products):
                    try:
                        # Robust title extraction
                        title_elem = product.select_one('.product-title') or product.find('h3') or product.find('h4')
                        title = title_elem.text.strip() if title_elem else None
                        if not title or title.lower() == "unknown product":
                            logger.warning(f"Skipping product {idx + 1} on page {page}: Invalid or missing title.")
                            continue
                        
                        # Price parsing
                        price_elem = product.select_one('.price')
                        price_text = price_elem.text.strip().replace('$', '') if price_elem else "0"
                        try:
                            price = float(price_text) if price_text.replace('.', '').isdigit() else 0
                        except ValueError:
                            logger.warning(f"Invalid price format for product {idx + 1} on page {page}: {price_text}")
                            continue  # Skip if price is invalid
                        
                        # Extract other fields
                        p_tags = product.find_all('p', style="font-size: 14px; color: #777;")
                        rating = "0.0 / 5"
                        colors = "0 Colors"
                        size = None
                        gender = None
                        
                        for p in p_tags:
                            text = p.text.strip()
                            if text.startswith("Rating:"):
                                rating = text.replace("Rating: ⭐ ", "").replace("Not Rated", "0.0 / 5")
                            elif text.endswith("Colors"):
                                colors = text
                            elif text.startswith("Size:"):
                                size = text.replace("Size: ", "")
                            elif text.startswith("Gender:"):
                                gender = text.replace("Gender: ", "")
                        
                        # Skip if critical fields are missing
                        if not size or not gender or price <= 0:
                            logger.warning(f"Skipping product {idx + 1} on page {page}: Missing critical fields or invalid price.")
                            continue
                        
                        all_data.append({
                            'Title': title,
                            'Price': price,
                            'Rating': rating,
                            'Colors': colors,
                            'Size': size,
                            'Gender': gender,
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'page_number': page
                        })
                        products_scraped += 1
                        logger.debug(f"Scraped product {idx + 1} on page {page}: {title} (Price: {price})")
                        
                    except AttributeError as e:
                        logger.warning(f"Failed to parse product {idx + 1} on page {page}: {str(e)}")
                        continue
                
                pages_scraped += 1
                logger.info(f"Page {page} scraped successfully. Total products collected so far: {products_scraped}")
                
            except requests.RequestException as e:
                logger.error(f"Failed to fetch page {page}: {str(e)}")
                continue
        
        if not all_data:
            logger.error("No data scraped from any page. Check CSS selectors or website accessibility.")
            return pd.DataFrame()
        
        df = pd.DataFrame(all_data)
        logger.info(f"Extraction completed. Total pages scraped: {pages_scraped}, Total products: {len(df)}")
        return df
    
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        return pd.DataFrame()
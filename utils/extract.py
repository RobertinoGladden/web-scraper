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
            # Correct URL construction based on page number
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
                logger.debug(f"HTML content: {soup.prettify()[:500]}")
                
                products = soup.select('.collection-card')
                if not products:
                    logger.warning(f"No products found on page {page}. Selector '.collection-card' may be incorrect.")
                    continue
                
                logger.info(f"Found {len(products)} products on page {page}")
                
                for idx, product in enumerate(products):
                    try:
                        # Robust title extraction with multiple fallbacks
                        title_elem = product.select_one('.product-title')
                        if not title_elem:
                            title_elem = product.find('h3') or product.find('h4') or product.find('div', class_=lambda x: x and 'title' in x.lower())
                        title = title_elem.text.strip() if title_elem else "Unknown Product"
                        
                        if title == "Unknown Product":
                            logger.warning(f"Product {idx + 1} on page {page} has no valid title. HTML snippet: {str(product)[:200]}")
                        
                        # Price parsing with fallback
                        price_text = product.select_one('.price').text.strip().replace('$', '') if product.select_one('.price') else "0"
                        price = 0
                        try:
                            price = float(price_text) if price_text.replace('.', '').isdigit() else 0
                        except ValueError:
                            logger.warning(f"Invalid price format for product {idx + 1} on page {page}: {price_text}")
                        
                        p_tags = product.find_all('p', style="font-size: 14px; color: #777;")
                        rating = "0.0 / 5" 
                        colors = "0 Colors" 
                        size = "Size: Unknown" 
                        gender = "Gender: Unknown" 
                        
                        for p in p_tags:
                            text = p.text.strip()
                            if text.startswith("Rating:"):
                                rating = text.replace("Rating: ⭐ ", "").replace("Not Rated", "0.0 / 5")
                            elif text.endswith("Colors"):
                                colors = text
                            elif text.startswith("Size:"):
                                size = text
                            elif text.startswith("Gender:"):
                                gender = text
                        
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
        if len(df) != 1000:
            logger.warning(f"Expected 1000 products, but only {len(df)} were scraped. Check for missing pages or products.")
        return df
    
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        return pd.DataFrame()
#!/usr/bin/env python3
"""
Level 2 Task 2: Data Scraper
A web scraper that extracts specific data from websites and saves it to CSV.
"""

import requests
import csv
import time
import re
from datetime import datetime
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False
    print(" BeautifulSoup4 not found. Install with: pip install beautifulsoup4")

class WebScraper:
    def __init__(self):
        """Initialize the web scraper"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.scraped_data = []
        self.delay = 1  # Delay between requests to be polite
    
    def get_page(self, url: str, timeout: int = 10) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page"""
        if not BS4_AVAILABLE:
            print(" BeautifulSoup4 is required for web scraping")
            return None
        
        try:
            print(f" Fetching: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f" Successfully fetched and parsed: {url}")
            return soup
            
        except requests.exceptions.RequestException as e:
            print(f" Request error for {url}: {e}")
            return None
        except Exception as e:
            print(f" Parsing error for {url}: {e}")
            return None
    
    def scrape_quotes_website(self, base_url: str = "http://quotes.toscrape.com") -> List[Dict]:
        """Scrape quotes from quotes.toscrape.com (demo site)"""
        quotes_data = []
        page = 1
        
        while True:
            url = f"{base_url}/page/{page}/"
            soup = self.get_page(url)
            
            if not soup:
                break
            
            quotes = soup.find_all('div', class_='quote')
            if not quotes:
                print(f" No more quotes found on page {page}")
                break
            
            print(f" Found {len(quotes)} quotes on page {page}")
            
            for quote in quotes:
                try:
                    text = quote.find('span', class_='text').get_text(strip=True)
                    author = quote.find('small', class_='author').get_text(strip=True)
                    tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
                    
                    quote_data = {
                        'text': text,
                        'author': author,
                        'tags': ', '.join(tags),
                        'page': page,
                        'scraped_at': datetime.now().isoformat()
                    }
                    quotes_data.append(quote_data)
                    
                except Exception as e:
                    print(f" Error parsing quote: {e}")
            
            page += 1
            time.sleep(self.delay)  # Be polite
        
        print(f" Scraped {len(quotes_data)} quotes total")
        return quotes_data
    
    def scrape_news_headlines(self, url: str) -> List[Dict]:
        """Generic news headline scraper"""
        soup = self.get_page(url)
        if not soup:
            return []
        
        headlines_data = []
        
        # Common selectors for headlines
        headline_selectors = [
            'h1', 'h2', 'h3',
            '.headline', '.title', '.post-title',
            '[class*="headline"]', '[class*="title"]',
            'article h2', 'article h3',
            '.entry-title', '.news-title'
        ]
        
        for selector in headline_selectors:
            headlines = soup.select(selector)
            if headlines:
                print(f" Found {len(headlines)} headlines with selector: {selector}")
                
                for i, headline in enumerate(headlines[:20]):  # Limit to first 20
                    try:
                        text = headline.get_text(strip=True)
                        if len(text) > 20:  # Filter out very short text
                            link = None
                            link_element = headline.find('a') or headline.find_parent('a')
                            if link_element and link_element.get('href'):
                                link = urljoin(url, link_element.get('href'))
                            
                            headline_data = {
                                'headline': text,
                                'link': link,
                                'selector_used': selector,
                                'position': i + 1,
                                'scraped_at': datetime.now().isoformat()
                            }
                            headlines_data.append(headline_data)
                    
                    except Exception as e:
                        print(f" Error parsing headline: {e}")
                
                break  # Use first successful selector
        
        # Remove duplicates based on headline text
        seen_headlines = set()
        unique_headlines = []
        for item in headlines_data:
            if item['headline'] not in seen_headlines:
                seen_headlines.add(item['headline'])
                unique_headlines.append(item)
        
        print(f" Scraped {len(unique_headlines)} unique headlines")
        return unique_headlines
    
    def scrape_product_info(self, url: str) -> List[Dict]:
        """Generic product information scraper"""
        soup = self.get_page(url)
        if not soup:
            return []
        
        products_data = []
        
        # Common selectors for products
        product_selectors = [
            '.product', '.item', '.listing',
            '[class*="product"]', '[class*="item"]'
        ]
        
        for selector in product_selectors:
            products = soup.select(selector)
            if products:
                print(f" Found {len(products)} products with selector: {selector}")
                
                for i, product in enumerate(products[:50]):  # Limit to first 50
                    try:
                        # Try to extract common product info
                        name = self._extract_text(product, [
                            '.name', '.title', '.product-name', '.product-title',
                            'h2', 'h3', 'h4', '.heading'
                        ])
                        
                        price = self._extract_text(product, [
                            '.price', '.cost', '.amount', '.value',
                            '[class*="price"]', '[class*="cost"]'
                        ])
                        
                        description = self._extract_text(product, [
                            '.description', '.summary', '.excerpt',
                            '.product-description', 'p'
                        ])
                        
                        # Extract link
                        link = None
                        link_element = product.find('a')
                        if link_element and link_element.get('href'):
                            link = urljoin(url, link_element.get('href'))
                        
                        if name:  # Only add if we found a name
                            product_data = {
                                'name': name,
                                'price': price,
                                'description': description,
                                'link': link,
                                'position': i + 1,
                                'scraped_at': datetime.now().isoformat()
                            }
                            products_data.append(product_data)
                    
                    except Exception as e:
                        print(f" Error parsing product: {e}")
                
                break  # Use first successful selector
        
        print(f" Scraped {len(products_data)} products")
        return products_data
    
    def _extract_text(self, element, selectors: List[str]) -> str:
        """Helper method to extract text using multiple selectors"""
        for selector in selectors:
            found = element.select_one(selector)
            if found:
                text = found.get_text(strip=True)
                if text and len(text) > 2:  # Must be meaningful text
                    return text
        return ""
    
    def save_to_csv(self, data: List[Dict], filename: str):
        """Save scraped data to CSV file"""
        if not data:
            print(" No data to save")
            return
        
        try:
            # Get all unique keys from all dictionaries
            all_keys = set()
            for item in data:
                all_keys.update(item.keys())
            
            fieldnames = sorted(list(all_keys))
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            print(f" Saved {len(data)} items to {filename}")
            
        except Exception as e:
            print(f" Error saving to CSV: {e}")
    
    def validate_url(self, url: str) -> bool:
        """Validate if URL is properly formatted"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

def get_scraping_choice():
    """Get user choice for scraping type"""
    print("\n Web Scraper - Choose what to scrape:")
    print("1.  Quotes (quotes.toscrape.com - demo site)")
    print("2.  News headlines (from any news website)")
    print("3.  Product information (from e-commerce sites)")
    print("4.  Custom scraping")
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("Invalid choice. Please enter 1, 2, 3, or 4.")

def get_valid_url():
    """Get and validate URL from user"""
    scraper = WebScraper()
    
    while True:
        url = input("Enter the website URL: ").strip()
        if scraper.validate_url(url):
            return url
        print(" Invalid URL format. Please enter a valid URL (including http:// or https://)")

def main():
    """Main function"""
    if not BS4_AVAILABLE:
        print(" This scraper requires BeautifulSoup4.")
        print("Install it with: pip install beautifulsoup4")
        return
    
    scraper = WebScraper()
    
    print(" Welcome to the Web Data Scraper!")
    print("This tool helps you extract data from websites and save it to CSV files.")
    print("\n Please be respectful when scraping websites:")
    print("- Check robots.txt")
    print("- Don't overwhelm servers with requests")
    print("- Respect website terms of service")
    
    choice = get_scraping_choice()
    
    try:
        if choice == '1':
            # Scrape quotes demo site
            print("\n Scraping quotes from quotes.toscrape.com...")
            data = scraper.scrape_quotes_website()
            if data:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"quotes_{timestamp}.csv"
                scraper.save_to_csv(data, filename)
        
        elif choice == '2':
            # Scrape news headlines
            print("\n News Headlines Scraper")
            print("Examples: https://news.ycombinator.com, https://www.bbc.com/news")
            url = get_valid_url()
            
            print(f"\n Scraping headlines from: {url}")
            data = scraper.scrape_news_headlines(url)
            
            if data:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                domain = urlparse(url).netloc.replace('.', '_')
                filename = f"headlines_{domain}_{timestamp}.csv"
                scraper.save_to_csv(data, filename)
        
        elif choice == '3':
            # Scrape product information
            print("\n Product Information Scraper")
            print("Note: Many e-commerce sites have anti-scraping measures")
            url = get_valid_url()
            
            print(f"\n Scraping products from: {url}")
            data = scraper.scrape_product_info(url)
            
            if data:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                domain = urlparse(url).netloc.replace('.', '_')
                filename = f"products_{domain}_{timestamp}.csv"
                scraper.save_to_csv(data, filename)
        
        elif choice == '4':
            # Custom scraping
            print("\n Custom Scraping")
            print("This will attempt to find common elements on the page")
            url = get_valid_url()
            
            soup = scraper.get_page(url)
            if soup:
                print("\n Analyzing page structure...")
                
                # Find common elements
                links = soup.find_all('a', href=True)[:20]
                headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])[:20]
                paragraphs = soup.find_all('p')[:20]
                
                custom_data = []
                
                print(f"Found {len(links)} links, {len(headings)} headings, {len(paragraphs)} paragraphs")
                
                # Extract links
                for i, link in enumerate(links):
                    text = link.get_text(strip=True)
                    href = urljoin(url, link.get('href'))
                    if text and len(text) > 3:
                        custom_data.append({
                            'type': 'link',
                            'text': text,
                            'url': href,
                            'position': i + 1
                        })
                
                # Extract headings
                for i, heading in enumerate(headings):
                    text = heading.get_text(strip=True)
                    if text and len(text) > 3:
                        custom_data.append({
                            'type': 'heading',
                            'text': text,
                            'tag': heading.name,
                            'position': i + 1
                        })
                
                if custom_data:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    domain = urlparse(url).netloc.replace('.', '_')
                    filename = f"custom_{domain}_{timestamp}.csv"
                    scraper.save_to_csv(custom_data, filename)
    
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
    except Exception as e:
        print(f" An unexpected error occurred: {e}")
    
    print("\n Scraping session completed!")

if __name__ == "__main__":
    main()



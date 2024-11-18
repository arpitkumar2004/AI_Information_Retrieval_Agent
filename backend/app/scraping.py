import requests
import re
from bs4 import BeautifulSoup
import logging
import sys
from typing import Dict, List, Optional
from urllib.parse import urlparse

# Set stdout encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Configure logging for debugging and error tracking
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize a session for reuse across requests
session = requests.Session()

def is_valid_url(url: str) -> bool:
    """
    Checks if the provided URL is valid and well-formed.
    
    Args:
        url (str): The URL to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)

def extract_emails(text: str) -> List[str]:
    """
    Extracts email addresses from the given text.
    
    Args:
        text (str): The text to extract emails from.
        
    Returns:
        List[str]: A list of extracted email addresses.
    """
    return list(set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)))

def extract_phone_numbers(text: str) -> List[str]:
    """
    Extracts phone numbers from the given text.
    
    Args:
        text (str): The text to extract phone numbers from.
        
    Returns:
        List[str]: A list of extracted phone numbers.
    """
    return list(set(re.findall(r'\b(?:\+?(\d{1,3})[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b', text)))

def extract_addresses(soup: BeautifulSoup) -> List[str]:
    """
    Extracts address-related information from the webpage.
    
    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the page.
        
    Returns:
        List[str]: A list of extracted address-related information.
    """
    address_keywords = ['address', 'location', 'headquarters', 'office', 'contact']
    address_texts = []
    div_texts = [div.get_text(strip=True) for div in soup.find_all('div')]
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
    
    for text in div_texts + paragraphs:
        if any(keyword in text.lower() for keyword in address_keywords):
            address_texts.append(text)
    return address_texts

def extract_social_links(soup: BeautifulSoup) -> List[str]:
    """
    Extracts social media links from the page.
    
    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the page.
        
    Returns:
        List[str]: A list of social media links.
    """
    social_platforms = ['facebook', 'twitter', 'linkedin', 'instagram']
    social_links = []
    
    for a in soup.find_all('a', href=True):
        link = a['href']
        if any(platform in link for platform in social_platforms):
            social_links.append(link)
    
    return social_links

def scrape_essential_info(url: str) -> Optional[Dict]:
    """
    Scrapes essential information from a given URL.
    
    Args:
        url (str): The URL of the webpage to scrape.
        
    Returns:
        dict: A dictionary containing the extracted metadata, contact information, and social media links.
    """
    if not is_valid_url(url):
        logging.error(f"Invalid URL: {url}")
        return None
    
    try:
        # Send a GET request to the URL using a session
        response = session.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            logging.error(f"Failed to retrieve content from {url} (Status Code: {response.status_code})")
            return None
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize a dictionary to store the essential information
        extracted_info = {
            'emails': extract_emails(response.text),
            'phone_numbers': extract_phone_numbers(response.text),
            'addresses': extract_addresses(soup),
            'social_links': extract_social_links(soup),
            'industry_sector': None,
            'website_url': url,
            'page_title': soup.title.string if soup.title else "No title"
        }
        
        # Extract industry sector or business category from meta description or meta keywords
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        
        if meta_description:
            extracted_info['industry_sector'] = meta_description.get('content', '')
        
        if not extracted_info['industry_sector'] and meta_keywords:
            extracted_info['industry_sector'] = meta_keywords.get('content', '')
        
        # Prepare the data for LLM use: Returning the data in a structured format
        result = {
            'metadata': {
                'website_url': extracted_info['website_url'],
                'page_title': extracted_info['page_title'],
                'industry_sector': extracted_info['industry_sector']
            },
            'contact_information': {
                'emails': extracted_info['emails'],
                'phone_numbers': extracted_info['phone_numbers'],
                'addresses': extracted_info['addresses']
            },
            'social_media': extracted_info['social_links']
        }
        
        # Return the structured data
        return result

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error occurred while scraping {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while scraping {url}: {e}")
        return None

if __name__ == "__main__":
    
    # Example test case to check if the module works as expected
    test_url = "https://www.ril.com/contact-us"
    scraped_data = scrape_essential_info(test_url)
    
    if scraped_data:
        logging.info(f"Successfully scraped data from {test_url}")
        print(scraped_data)
    else:
        logging.error(f"Failed to scrape data from {test_url}")

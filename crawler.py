import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import urljoin
import logging
from typing import List, Dict, Optional

class WebCrawler:
    def __init__(self):
        # List of proxies
        self.proxies = [
            "46.232.112.77:2534:97tb6:ezbgofao",
            "91.231.142.146:2534:97tb6:ezbgofao",
            "91.231.143.3:2534:97tb6:ezbgofao",
            "91.231.143.32:2534:97tb6:ezbgofao",
            "91.231.143.32:2534:97tb6:ezbgofao",
            "91.239.187.138:2534:97tb6:ezbgofao",
            "170.81.199.194:2534:97tb6:ezbgofao",
            "188.119.114.20:2534:97tb6:ezbgofao",
            "188.119.114.58:2534:97tb6:ezbgofao",
            "191.102.132.184:2534:97tb6:ezbgofao",
            "194.105.159.69:2534:97tb6:ezbgofao",
            "206.162.246.20:2534:97tb6:ezbgofao",
            "206.162.250.213:2534:97tb6:ezbgofao",
            "216.177.134.32:2534:97tb6:ezbgofao"
        ]
        
        # Common user agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def _get_random_proxy(self) -> Dict[str, str]:
        """Get a random proxy from the list."""
        proxy = random.choice(self.proxies)
        ip, port, username, password = proxy.split(':')
        return {
            'http': f'http://{username}:{password}@{ip}:{port}',
            'https': f'http://{username}:{password}@{ip}:{port}'
        }

    def _get_headers(self) -> Dict[str, str]:
        """Generate random headers for the request."""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def get_sublinks(self, url: str, max_retries: int = 3) -> Optional[List[str]]:
        """Extract all sublinks from the given URL.
        
        Args:
            url: The URL to crawl
            max_retries: Maximum number of retry attempts
            
        Returns:
            List of sublinks found on the page, or None if failed
        """
        retry_count = 0
        while retry_count < max_retries:
            try:
                # Get random proxy and headers
                proxy = self._get_random_proxy()
                headers = self._get_headers()
                
                # Make the request
                response = requests.get(
                    url,
                    proxies=proxy,
                    headers=headers,
                    timeout=10
                )
                response.raise_for_status()
                
                # Parse the HTML
                soup = BeautifulSoup(response.text, 'lxml')
                
                # Find all links
                links = set()
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        # Convert relative URLs to absolute URLs
                        absolute_url = urljoin(url, href)
                        links.add(absolute_url)
                
                self.logger.info(f'Successfully extracted {len(links)} links from {url}')
                return list(links)
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f'Attempt {retry_count + 1} failed: {str(e)}')
                retry_count += 1
                
        self.logger.error(f'Failed to crawl {url} after {max_retries} attempts')
        return None

def main():
    # Example usage
    crawler = WebCrawler()
    url = input('Enter the URL to crawl: ')
    
    links = crawler.get_sublinks(url)
    if links:
        print('\nFound links:')
        for link in sorted(links):
            print(f'- {link}')
    else:
        print('Failed to extract links')

if __name__ == '__main__':
    main()
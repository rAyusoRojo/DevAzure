import urllib.request
import urllib.error
import urllib.parse
import json
from http.client import HTTPResponse
from typing import Dict, Optional

class WebScraper:
    def __init__(self):
        # Add common headers to mimic a regular browser request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetches content from a given URL using proper error handling
        """
        try:
            # Create a request object with headers
            request = urllib.request.Request(url, headers=self.headers)
            
            # Perform the request
            with urllib.request.urlopen(request) as response:
                if not isinstance(response, HTTPResponse):
                    return None
                
                # Read and decode the response
                content = response.read().decode('utf-8')
                return content
                
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"URL Error: {e.reason}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        
        return None

    def save_content(self, content: str, filename: str) -> bool:
        """
        Saves the content to a file
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return False

def main():
    # Example usage with a public API
    scraper = WebScraper()
    
    # Using a public API as an example
    sample_url = "https://www.examtopics.com/discussions/microsoft/view/151778-exam-az-900-topic-1-question-474-discussion"
    print("Fetching content...")
    
    content = scraper.fetch_page(sample_url)
    
    if content:
        # Save the raw content
        scraper.save_content(content, 'raw_content.txt')
        
        # Parse and save formatted JSON
        try:
            data = json.loads(content)
            formatted_content = json.dumps(data, indent=2)
            scraper.save_content(formatted_content, 'formatted_content.json')
            print("Content successfully downloaded and saved!")
            print("\nSample of retrieved content:")
            print(formatted_content)
        except json.JSONDecodeError:
            print("Could not parse JSON content")
    else:
        print("Failed to fetch content")

if __name__ == "__main__":
    main()
import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_verse():
    url = "https://alkitab.mobi/renungan/rh/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Find the div that contains "Nas:"
        nas_label = soup.find(text=lambda t: "Nas:" in t)
        nas_div = nas_label.find_parent('div')
        
        # The verse reference is usually inside a bold or link tag within that div
        reference = nas_div.find('a').text.strip()
        
        # The verse text is the text following the reference
        # We clean up extra whitespace and newlines
        full_text = nas_div.text.replace("Nas:", "").replace(reference, "").strip()

        data = {
            "reference": reference,
            "verse": full_text
        }

        # Save to data directory
        os.makedirs('data', exist_ok=True)
        with open('data/verse.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully scraped: {reference}")
    except Exception as e:
        print(f"Error scraping: {e}")

if __name__ == "__main__":
    scrape_verse()

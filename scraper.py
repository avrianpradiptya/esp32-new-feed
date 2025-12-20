import requests
from bs4 import BeautifulSoup
import json
import os
import re

def scrape_verse():
    url = "https://alkitab.mobi/renungan/rh/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Get the main content text
        nas_label = soup.find(text=lambda t: "Nas:" in t)
        nas_div = nas_label.find_parent('div')
        full_text = nas_div.text

        # Logic: Find the line that has a book reference in parentheses (e.g. "(Bilangan 9:16)")
        # This regex looks for text ending with (Book Name Chapter:Verse)
        pattern = r"\n\s*(.*?\(.*?\d+:\d+.*?\))"
        match = re.search(pattern, full_text)

       if match:
            # We grab the match and strip the "Nas:" prefix specifically
            final_content = match.group(1).replace("Nas:", "").strip()
        else:
            # Fallback cleaning
            lines = full_text.split('\n')
            raw_line = next((l.strip() for l in lines if "(" in l and ":" in l), "")
            final_content = raw_line.replace("Nas:", "").strip()

        data = { "content": final_content }

        os.makedirs('data', exist_ok=True)
        with open('data/verse.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print(f"Success: {final_content}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_verse()

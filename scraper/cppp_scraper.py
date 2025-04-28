# scraper/cppp_scraper.py

import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_cppp():
    url = "https://etenders.gov.in/eprocure/app?page=FrontEndLatestActiveTenders&service=page"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    tenders = []

    # Locate tender table rows
    table = soup.find("table", {"class": "table table-striped"})
    if table:
        rows = table.find_all("tr")[1:]  # Skip table header
        
        for row in rows:
            columns = row.find_all("td")
            if len(columns) >= 5:
                tender = {
                    "title": columns[0].text.strip(),
                    "authority": columns[1].text.strip(),
                    "emd": "N/A",  # EMD not available on list page
                    "deadline": columns[4].text.strip(),
                    "scope": "Scope details inside tender document."
                }
                tenders.append(tender)
    
    # Save tenders to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/tenders.json", "w") as f:
        json.dump(tenders, f, indent=4)
    
    print(f"✅ Scraped {len(tenders)} tenders from CPPP portal.")

if __name__ == "__main__":
    scrape_cppp()

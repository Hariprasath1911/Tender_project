import requests
from bs4 import BeautifulSoup
import json

def scrape_cppp():
    url = "https://etenders.gov.in/eprocure/app"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Dummy tenders (you can change this as per real structure)
    tenders = []
    for i in range(5):
        tender = {
            "title": f"Tender {i+1}",
            "scope": f"Supply of items {i+1}",
            "deadline": "2025-05-30",
            "emd": "5000 INR"
        }
        tenders.append(tender)
    
    # Save tenders
    with open('data/tenders.json', 'w') as f:
        json.dump(tenders, f, indent=4)

if __name__ == "__main__":
    scrape_cppp()

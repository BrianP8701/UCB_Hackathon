import requests
import re

from app.services.PdfService import PdfService

pdf_service = PdfService()

def mimic_request():
    url = "https://www.nar.realtor/code-of-ethics-and-arbitration-manual/forms"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Process the response here
        return response.text
    else:
        print("Failed to fetch the URL")

def find_pdf_links(text):
    return re.findall(r'https://\S+\.pdf', text)

text = mimic_request()
print(text)
pdf_links = find_pdf_links(text)
print(pdf_links)
print(len(pdf_links))
pdf_service.download_pdfs(pdf_links, 'data/raw/pdfs/nar_realtor', "nar_realtor")

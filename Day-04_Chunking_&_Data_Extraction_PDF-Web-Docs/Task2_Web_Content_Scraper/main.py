import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json

load_dotenv()
class Webscraper:
    def __init__ (self,url):

        self.url = url
        print(f"URL for scrape: {self.url}")
        self.content = ""

    def scrape_quotes(self):
        page = requests.get(self.url)
        # print(page.text)
        soup = BeautifulSoup(page.content, "html.parser")
        webpage_data = soup.find(id="hockey")
        header_data = webpage_data.find("div", class_="col-md-12")
        title_element = header_data.find("h1").text
        print(title_element)
        table_data = webpage_data.find("table", class_="table")
        # print(table_data)
        headers = [th.text.strip() for th in table_data.find_all("th")]

        # Extract rows
        # Extract row data
        rows = []
        for tr in table_data.find_all("tr")[1:]:  # skip header row
            cells = tr.find_all("td")

            if not cells:
                continue

            row_data = {}
            for header, cell in zip(headers, cells):
                text = cell.get_text(strip=True)
                row_data[header] = text
                rows.append(row_data)

        result = {
            "url": self.url,
            "website_title":title_element,
            "data":rows
        }
        print(result)




read_website_data = Webscraper("https://www.scrapethissite.com/pages/forms/")
read_website_data.scrape_quotes()
# readPdf.add_context()

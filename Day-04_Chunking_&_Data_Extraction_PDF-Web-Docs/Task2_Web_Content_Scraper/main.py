import requests
from bs4 import BeautifulSoup

class Webscraper:
    def __init__(self, url):
        self.url = url
        print(f"URL for scrape: {self.url}")

    def scrape_table_data(self):
        try:
            page = requests.get(self.url)
            page.raise_for_status()  # ✅ HTTP error handling
        except requests.RequestException as e:
            print("Request failed:", e)
            return

        soup = BeautifulSoup(page.content, "html.parser")

        webpage_data = soup.find(id="hockey")
        if not webpage_data:
            print("Could not find hockey section")
            return

        header_data = webpage_data.find("div", class_="col-md-12")
        title_element = header_data.find("h1").get_text(strip=True)
        print("Page Title:", title_element)

        table_data = webpage_data.find("table", class_="table")
        if not table_data:
            print("Table not found")
            return

        headers = [th.get_text(strip=True) for th in table_data.find_all("th")]

        rows = []
        for tr in table_data.find_all("tr")[1:]:  # skip header row
            cells = tr.find_all("td")
            if not cells:
                continue

            row_data = {}
            for header, cell in zip(headers, cells):
                row_data[header] = cell.get_text(strip=True)

            rows.append(row_data)  # ✅ correct placement

        result = {
            "url": self.url,
            "website_title": title_element,
            "data": rows
        }

        print(result)


read_website_data = Webscraper("https://www.scrapethissite.com/pages/forms/")
read_website_data.scrape_table_data()

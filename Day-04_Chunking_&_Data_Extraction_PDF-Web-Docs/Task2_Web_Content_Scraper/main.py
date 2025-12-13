import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

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





read_website_data = Webscraper("https://www.scrapethissite.com/pages/forms/")
read_website_data.scrape_quotes()
# readPdf.add_context()

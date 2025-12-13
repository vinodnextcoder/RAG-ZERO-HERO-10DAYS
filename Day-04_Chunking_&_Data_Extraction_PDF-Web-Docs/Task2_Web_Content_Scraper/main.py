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
        result = soup.find(id="hockey")
        print(result)





read_website_data = Webscraper("https://www.scrapethissite.com/pages/forms/")
read_website_data.scrape_quotes()
# readPdf.add_context()

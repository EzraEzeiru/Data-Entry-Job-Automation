import bs4
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

CHROME_DRIVER_PATH = "/Users/ezeiruezra/Development/chromedriver"
s = Service(CHROME_DRIVER_PATH)
URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
headers = {
    "Accept-Language": "en-US,en;q=0.9",

    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36"
}

response = requests.get(url=URL, headers=headers)
zillow_webpage = response.text

soup = bs4.BeautifulSoup(zillow_webpage, "html.parser")
home_address = soup.findAll(name="address", class_="list-card-addr")
all_addresses = []
for address in home_address:
    text_address = address.getText()
    all_addresses.append(text_address)

home_prices = soup.findAll(name="div", class_="list-card-price")
all_prices = []
for price in home_prices:
    int_price = price.getText().strip("+ 1bbd/mo")
    all_prices.append(int_price)

home_url_links = soup.find_all(name="a", class_="list-card-link")
all_links = []
for link in home_url_links[0:-1:2]:
    url = link.get("href")
    if '/b' in url:
        url = f"http://www.zillow.com{url}"
    all_links.append(url)


class DataEntry:
    def __init__(self):
        self.driver = webdriver.Chrome(service=s)

    def fill_form(self, price, address, link):
        self.driver.get(
            "https://docs.google.com/forms/d/e/1FAIpQLSedBfr7BZI5PiiSwdDptDTI2XFfJ-yl6k4hYSZQr77E2V9TmQ/viewform?usp=sf_link")
        enter_address = self.driver.find_element(By.XPATH,
                                                 value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        enter_address.send_keys(f"{address}")
        enter_price = self.driver.find_element(By.XPATH,
                                               value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        enter_price.send_keys(f"{price}")
        enter_link = self.driver.find_element(By.XPATH,
                                              value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        enter_link.send_keys(f"{link}")
        submit_button = self.driver.find_element(By.XPATH,
                                                 value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
        submit_button.click()


my_form = DataEntry()
for num in range(len(all_links)):
    the_price = all_prices[num]
    the_address = all_addresses[num]
    the_links = all_links[num]
    my_form.fill_form(the_price, the_address, the_links)

from celery import shared_task
from .models import ScrapingJob
from selenium import webdriver
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as Chromeservice
from webdriver_manager.chrome import ChromeDriverManager
import time
# import logging
import requests
from selenium.webdriver.chrome.options import Options

# logger = logging.getLogger(__name__)
class CoinMarketCap:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Chromeservice(ChromeDriverManager().install()))
        # logger.info("WebDriver initialized.")
        # print("Initializing CoinMarketCap class...")
        # self.driver = GeckoDriverManager().install()
        # print(f"GeckoDriver path: {self.driver_path}")
        # self.driver = webdriver.Firefox(service=FirefoxService(self.driver_path))

    def fetch_coin_data(self,coin_name):
        options = Options()
        options.add_argument("--headless")  # Ensure the browser runs headlessly
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        url = f'https://coinmarketcap.com/currencies/{coin_name.lower}/ '
        self.driver.get(url)
        time.sleep(10)

        data ={}

        try:
            data['price'] = float(self.driver.find_element('xpath','/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/section/div/div[2]/span').text.replace('$','').replace(',',''))
            # logger.info(f"{coin_name} price: {data['price']}")
            print(data['price'])
            data['price_change'] = float(self.driver.find_element('xpath','//*[@id="section-coin-overview"]/div[2]/div/div/p,').text.replace('%',''))
            # logger.info(f"{coin_name} price change: {data['price_change']}")
            print(data['price_change'])
            data['market_cap'] = float(self.driver.find_element('xpath','//*[@id="section-coin-stats"]/div/dl/div[1]/div[1]/dt/div[1]').text.replace('$','').replace(',',''))
            # logger.info(f"{coin_name} market cap: {data['market_cap']}")
            print(data['market_cap'])
            data['market_cap_rank'] = int(self.driver.find_element('xpath','//*[@id="section-coin-stats"]/div/dl/div[1]/div[2]/div/span').text.replace('#', ''))
            # logger.info(f"{coin_name} market cap rank: {data['market_cap_rank']}")
            print(data['market_cap_rank'])
            data['volume'] = int(self.driver.find_element('xpath','//*[@id="section-coin-stats"]/div/dl/div[2]/div[1]/dd').text.replace('$', '').replace(',', ''))
            # logger.info(f"{coin_name} volume: {data['volume']}")
            print(data['volume'])
            data['volume_rank'] = int(self.driver.find_element('xpath','//*[@id="section-coin-stats"]/div/dl/div[2]/div[2]/div/span').text.replace('#', ''))
            # logger.info(f"{coin_name} volume rank: {data['volume_rank']}")
            print(data['volume_rank'])
            data['volume_change'] = float(self.driver.find_element('xpath','//*[@id="section-coin-stats"]/div/dl/div[3]/div/dd').text.replace('%', ''))
            # logger.info(f"{coin_name} volume change: {data['volume_change']}")
            print(data['volume_change'])
            data['circulating_supply'] = int(self.driver.find_element('xpath','//*[@id="section-coin-stats"]/div/dl/div[4]/div[1]/dd').text.replace(',', ''))
            # logger.info(f"{coin_name} circulating supply: {data['circulating_supply']}")
            print(data['circulating_supply'])
            data['total_supply'] = int(self.driver.find_element('xpath','//*[@id="section-coin-stats"]/div/dl/div[5]/div/dd').text.replace(',', ''))
            # logger.info(f"{coin_name} total supply: {data['total_supply']}")
            print(data['total_supply'])
            data['diluted_market_cap'] = int(self.driver.find_element('//*[@id="section-coin-stats"]/div/dl/div[7]/div/dd').text.replace('$', '').replace(',', ''))
            # logger.info(f"{coin_name} diluted market cap: {data['diluted_market_cap']}")
            print(data['diluted_market_cap'])

            website = self.driver.find_element('xpath','/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[2]/div[2]/div/div[1]/a').text
            data['official_links'] = [{'name':'website','link':website}]

            twitter = self.driver.find_element('xpath','/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[3]/div[2]/div/div[1]/a')
            reddit = self.driver.find_element('xpath','/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[2]/section[2]/div/div[2]/div[3]/div[2]/div/div[2]/a')
            data['socials']=[{'name':'twitter','url':twitter},{'name':'reddit','url':reddit}]
        except Exception as e:
            data['error']=str(e)
            # logger.error(f"Error fetching data for {coin_name}: {str(e)}")

        return data
    
    def close(self):
        #  logger.info("Closing the browser...")
         print("Closing the browser...")
         self.driver.quit()
    


@shared_task
def scrape_coin_data(coins, job_id):
    job = ScrapingJob.objects.get(job_id=job_id)
    results = []

    scraper = CoinMarketCap()
    for coin in coins:
        data = scraper.fetch_coin_data(coin)
        results.append({'coin':coin,'output':data})
        # logger.info(f"Scraped data for {coin}: {data}")

    scraper.close()

    job.result = results
    job.status = 'Completed'
    job.save()
    # logger.info(f"Job {job_id} completed with results: {results}")
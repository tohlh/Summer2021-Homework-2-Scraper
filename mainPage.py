import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import videoPage
import channelPage
import dbAdapter

da = dbAdapter.adapter()

# Scrape some of the channels on YouTube main page
class mainPageScraper():
    def scrapeMainPage(self, limit):
        baseUrl = 'https://www.youtube.com'
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        driver.get(baseUrl)

        for x in range(10000, 500000, 10000):
            script = 'window.scrollTo(1, ' + str(x) + ');'
            driver.execute_script(script)
            time.sleep(1)

        currChannelLinksNum = da.getTotalChannelsToScrape()
        videoThumbnails = driver.find_elements_by_xpath('//*[@id="text"]/a')
        for x in videoThumbnails:
            currChannelLink = str(x.get_attribute('href'))
            if currChannelLink != None and currChannelLink[0:26] == 'https://www.youtube.com/c/' and currChannelLinksNum <= limit:
                source = requests.get(currChannelLink).text
                soup = BeautifulSoup(source, 'html.parser')
                id_meta = soup.find('meta', {'itemprop': 'channelId'})
                if id_meta == None:
                    continue
                id = id_meta['content']
                da.addChannelToQueue(id)
                if currChannelLinksNum != da.getTotalChannelsToScrape():
                    currChannelLinksNum = da.getTotalChannelsToScrape()
                print('Found {0} links.'.format(currChannelLinksNum))
                time.sleep(1)
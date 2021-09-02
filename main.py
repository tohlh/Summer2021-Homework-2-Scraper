import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import videoPage
import channelPage
import dbAdapter

vs = videoPage.videoScraper()
cs = channelPage.channelScraper()

# Scrape some of the creators on YouTube main page
def mainPageScraper():
    baseUrl = 'https://www.youtube.com'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    vs = videoPage.videoScraper()
    cs = creatorPage.creatorScraper
    videoLinksDump = open('videoLinksDump.txt', 'w')
    driver.get(baseUrl)
    ret = 0

    for x in range(10000, 100000, 10000):
        script = 'window.scrollTo(1, ' + str(x) + ');'
        driver.execute_script(script)
        time.sleep(1)

    videoThumbnails = driver.find_elements_by_xpath('//*[@id="text"]/a')
    for x in videoThumbnails:
        if (str(x.get_attribute('href')) != 'None'):
            videoLinksDump.write(str(x.get_attribute('href')) + '\n')
            ret += 1

    return ret

def main():
    #dbAdapter.connectDB()
    #initialLinksNum = mainPageScraper()
    #print('Found ' + str(initialLinksNum) + ' initial links.')
    #vs.scrapeVideo('8NK1I6S_vFs')
    cs.scrapeChannel('https://www.youtube.com/user/LinusTechTips')

if __name__ == "__main__":
    main()
